# -*- coding: utf-8 -*-

##    This file is part of Gertrude.
##
##    Gertrude is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 3 of the License, or
##    (at your option) any later version.
##
##    Gertrude is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with Gertrude; if not, see <http://www.gnu.org/licenses/>.

from constants import *
from functions import *
from facture import *
from sqlobjects import Parent
from cotisation import CotisationException
from ooffice import *

class AttestationModifications(object):
    def __init__(self, who, debut, fin):
        self.multi = False
        self.template = 'Attestation paiement.odt'
        if isinstance(who, list):
            self.email_subject = u"Attestations de paiement %s-%s %d" % (months[debut.month - 1], months[fin.month - 1], debut.year)
            self.inscrits = [inscrit for inscrit in who if inscrit.GetInscriptions(debut, fin)]
            self.email_to = None
        else:
            self.email_subject = u"Attestation de paiement %s %s %s-%s %d" % (who.prenom, who.nom, months[debut.month - 1], months[fin.month - 1], debut.year)
            self.inscrits = [who]
            self.email_to = None
            # TODO self.email_to = list(set([parent.email for parent in who.parents.values() if parent.email]))
        self.default_output = self.email_subject + ".odt"
        self.debut, self.fin = debut, fin
        self.email = True
        self.site = None
        self.email_text = "Accompagnement attestation paiement.txt"
        
    def execute(self, filename, dom):
        if filename != 'content.xml':
            return None
        
        errors = {}
        tresorier = ""
        directeur = ""
        bureau = Select(creche.bureaux, today)
        if bureau:
            tresorier = bureau.tresorier
            directeur = bureau.directeur
        
        # print dom.toprettyxml()
        doc = dom.getElementsByTagName("office:text")[0]
        templates = doc.getElementsByTagName('text:section')
        for template in templates:
            doc.removeChild(template)
        
        for inscrit in self.inscrits:
            facture_debut = facture_fin = None
            date = self.debut
            heures_facturees = 0.0
            total = 0.0
            site = None
            try:
                while date <= self.fin:
                    facture = Facture(inscrit, date.year, date.month)
                    site = facture.site
                    if facture.total != 0:
                        if facture_debut is None:
                            facture_debut = date
                        facture_fin = getMonthEnd(date)
                        total += facture.total
                        heures_facturees += facture.heures_facturees
                    date = getNextMonthStart(date)
            except CotisationException, e:
                errors[GetPrenomNom(inscrit)] = e.errors
                continue
            
            if facture_debut is None:
                continue
                
            # Les champs du recu
            fields = GetCrecheFields(creche) +  GetInscritFields(inscrit) + [
                    ('de-debut', '%s %d' % (GetDeMoisStr(facture_debut.month - 1), facture_debut.year)),
                    ('de-fin', '%s %d' % (GetDeMoisStr(facture_fin.month - 1), facture_fin.year)),
                    ('tresorier', tresorier),
                    ('directeur', directeur),
                    ('date', '%.2d/%.2d/%d' % (today.day, today.month, today.year)),
                    ('heures-facturees', '%.2f' % heures_facturees),
                    ('total', '%.2f' % total),
                    ('site', GetNom(site))
                    ]
    
            if inscrit.sexe == 1:
                fields.append(('ne-e', u"né"))
            else:
                fields.append(('ne-e', u"née"))
            
            for template in templates:
                section = template.cloneNode(1)
                doc.appendChild(section)
                ReplaceTextFields(section, fields)
                
        return errors

