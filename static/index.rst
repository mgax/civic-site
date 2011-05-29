CivicDB este o bază de date cu informații despre administrația publică din
România. Datele sunt fost obținute din surse publice, de către diverse
persoane și organizații, și sunt adunate aici pentru a ușura munca oricui are
nevoie de acces la aceste informații.

Pentru interogări puteți folosi `pagina de test`_ sau `serviciul SPARQL`_.
Sunt disponibile următoarele seturi de date:

 * :ref:`alegeri-2008` - participanți și rezultate

.. _`pagina de test`: /test
.. _`serviciul SPARQL`: /sparql

.. TODO datele sunt libere?
.. TODO licență pentru software, paginile din site și baza de date


Tehnologie
==========
Baza de date este construită folosind tehnologii `semantic web`_. Datele sunt
stocate sub formă de tripleți RDF_ într-o bază de date 4store_ și pot fi
interogate prin SPARQL_. Arhitectura aceasta prezintă câteva avantaje față de
o bază de date relațională:

`Stocare uniformă a datelor`
   Totul este reprezentat prin tripleți; nu e nevoie de JOIN-uri peste multe
   tabele

`Evoluție naturală`
   Adunăm date din surse diverse care nu se potrivesc întotdeauna pe aceleași
   șabloane. Putem extinde structura datelor fără să fie nevoie de migrări ale
   schemei de tabele.

`Partiționarea pe modele`
   Păstrăm separate dataset-urile din surse diferite și le actualizăm
   independent. Dataset-urile pot fi downloadate sub formă de fișiere
   `RDF/XMl`.

`API de interogare standard`
    Folosim limbajul SPARQL_, standard în lumea `semantic web`, ceea ce ne
    scutește de nevoia de a construi un API care să acopere toată complexitatea
    structurii datelor.

.. _`semantic web`: http://www.w3.org/standards/semanticweb/
.. _RDF: http://www.w3.org/standards/techs/rdf
.. _4store: http://4store.org/
.. _SPARQL: http://www.w3.org/standards/techs/sparql


.. toctree::
   :hidden:
   :glob:

   datasets/*
