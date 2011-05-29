.. _alegeri-2008:

Alegerile din 2008
==================

De la `alegeri.tv`_ am primit tabele cu toți participanții la alegerile din
2008. Momentan în baza de date sunt doar candidații la primării, partidele
din care fac parte și care le-au susținut candidatura, și rezulatul obținut
în turul 1 și 2.

.. _`alegeri.tv`: http://www.alegeri.tv/


Urmează o descriere a termenilor RDF folosiți în baza de date. Pentru fiecare
clasă sunt enumerate proprietățile, sub formă de predicat RDF urmat de tipul
de date al valorilor. De exemplu, candidații (`?person`) au tipul
`civic:Person`_::

    ?person rdf:type civic:Person .

Numele candidatului (`?name`) este specificat cu proprietatea `foaf:name`::

    ?person foaf:name ?name .


.. _`civic:Person`:

``civic:Person`` - candidat la alegeri
--------------------------------------

``foaf:name`` `Literal`
    Nume și prenume

``civic:memberInParty`` `civic:Party`_
    Membru în partid


.. _`civic:Party`:

``civic:Party`` - partid politic
--------------------------------

``rdfs:label`` `Literal`
    Numele partidului


.. _`civic:Election`:

``civic:Election`` - tur de alegeri
-----------------------------------

``rdfs:label`` `Literal`
    Numele turului de alegeri


.. _`civic:Constituency`:

``civic:Constituency`` - circumscripție electorală
--------------------------------------------------

.. TODO civic:Constituency does not exist in RDF!

``rdfs:label`` `Literal`
    Numele circumscripției


.. _`civic:Campaign`:

``civic:Campaign`` - campania unui candidat într-o alegere
----------------------------------------------------------

``civic:candidate`` `civic:Person`_
    Persoana care candidează

``civic:party`` `civic:Party`_
    Partidul care susține campania

``civic:election`` `civic:Election`_
    Turul de alegeri pentru care are loc campania

``civic:voteFraction`` `Literal`
    Procentul din voturi câștigat (între `0.0` și `1.0`)

``civic:win`` `Literal`
    Campanie câștigată (da/nu)

``civic:constituency`` `civic:Constituency`_
    Circumscripția în care are loc campania
