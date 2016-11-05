# -*- coding: utf-8 -*-

#    This file is part of Gertrude.
#
#    Gertrude is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Gertrude is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Gertrude; if not, see <http://www.gnu.org/licenses/>.

from constants import *
from functions import *
from facture import *
from ooffice import *


class CoordonneesModifications(object):
    def __init__(self, site, date):
        self.multi = False
        self.site = site
        if date is None:
            self.date = today
        else:
            self.date = date
        self.email = None
        if IsTemplateFile("Coordonnees parents.ods"):
            self.template = "Coordonnees parents.ods"
            self.default_output = u"Coordonnees parents %s.ods" % GetDateString(self.date, weekday=False)
        else:
            self.template = 'Coordonnees parents.odt'
            self.default_output = u"Coordonnees parents %s.odt" % GetDateString(self.date, weekday=False)

    def execute(self, filename, dom):
        if self.template == "Coordonnees parents.ods":
            return self.execute_ods(filename, dom)
        else:
            return self.execute_odt(filename, dom)

    def execute_ods(self, filename, dom):
        if filename != 'content.xml':
            return None

        errors = {}
        spreadsheet = dom.getElementsByTagName('office:spreadsheet')[0]
        table = spreadsheet.getElementsByTagName("table:table")[0]
        lignes = table.getElementsByTagName("table:table-row")
        template = lignes[1]
        for inscrit in GetEnfantsTriesParPrenom():
            inscription = inscrit.GetInscription(self.date)
            if inscription and (self.site is None or inscription.site == self.site):
                inscrit_fields = GetInscritFields(inscrit)
                for parent in inscrit.famille.parents:
                    if parent:
                        fields = inscrit_fields + GetParentFields(parent)
                        line = template.cloneNode(1)
                        ReplaceFields(line, fields)
                        table.insertBefore(line, template)
                        inscrit_fields = [(field[0], "") for field in inscrit_fields]
        table.removeChild(template)
        return errors

    def execute_odt(self, filename, dom):
        # print dom.toprettyxml()
        if filename != 'content.xml':
            return None

        fields = GetCrecheFields(creche)
        fields.append(('date', '%.2d/%.2d/%d' % (self.date.day, self.date.month, self.date.year)))
        ReplaceTextFields(dom, fields)
        
        for table in dom.getElementsByTagName('table:table'):
            if table.getAttribute('table:name') == 'Enfants':                
                template = table.getElementsByTagName('table:table-row')[1]
                #print template.toprettyxml()
                for inscrit in GetEnfantsTriesParPrenom():
                    inscription = inscrit.GetInscription(self.date) 
                    if inscription and (self.site is None or inscription.site == self.site):
                        line = template.cloneNode(1)
                        referents = [GetPrenomNom(referent) for referent in inscrit.famille.referents]
                        parents = [GetPrenomNom(parent) for parent in inscrit.famille.parents if parent is not None]
                        ReplaceTextFields(line, [('prenom', inscrit.prenom),
                                                 ('parents', parents),
                                                 ('referents', referents),
                                                 ('commentaire', None)])
                        phoneCell = line.getElementsByTagName('table:table-cell')[2]
                        phoneTemplate = phoneCell.getElementsByTagName('text:p')[0]
                        phones = { } # clé: [téléphone, initiales, ?travail]
                        emails = set()
                        for parent in inscrit.famille.parents:
                            if parent:
                                emails.add(parent.email)
                                for phoneType in ["domicile", "portable", "travail"]:
                                    phone = getattr(parent, "telephone_" + phoneType)
                                    if phone:
                                        if phone in phones.keys():
                                            phones[phone][1] = ""
                                        else:
                                            phones[phone] = [phone, GetInitialesPrenom(parent), phoneType=="travail"]
                        for phone, initiales, phoneType in phones.values():
                            if initiales and phoneType:
                                remark = "(%s travail)" % initiales
                            elif initiales:
                                remark = "(%s)" % initiales
                            elif phoneType:
                                remark = "(travail)"
                            else:
                                remark = ""
                            phoneLine = phoneTemplate.cloneNode(1)
                            ReplaceTextFields(phoneLine, [('telephone', phone),
                                                          ('remarque', remark)])
                            phoneCell.insertBefore(phoneLine, phoneTemplate)
                        phoneCell.removeChild(phoneTemplate)
                        emailCell = line.getElementsByTagName('table:table-cell')[3]
                        emailTemplate = emailCell.getElementsByTagName('text:p')[0]
                        for email in emails:
                            emailLine = emailTemplate.cloneNode(1)
                            ReplaceTextFields(emailLine, [('email', email)])
                            emailCell.insertBefore(emailLine, emailTemplate)
                        emailCell.removeChild(emailTemplate)
                        table.insertBefore(line, template)
                table.removeChild(template)

            if table.getAttribute('table:name') == 'Employes':
                template = table.getElementsByTagName('table:table-row')[0]
                #print template.toprettyxml()
                for salarie in creche.salaries:
                    if 1:  # TODO
                        line = template.cloneNode(1)
                        ReplaceTextFields(line, [('prenom', salarie.prenom),
                                                 ('nom', salarie.nom),
                                                 ('domicile', salarie.telephone_domicile),
                                                 ('portable', salarie.telephone_portable)])
                        table.insertBefore(line, template)
                table.removeChild(template)

        return None
