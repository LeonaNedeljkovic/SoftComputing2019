# SoftComputing2019

## Pokretanje istreniranog modela

<b>Pre pokretanja aplikacije skinuti sleće fajlove i smestiti ih u folder "data":</b><br/>
<ul>
  <li><b>RC_2013-06</b> (https://drive.google.com/open?id=1hZ1ZgnGctEcoODzi1qI19_qYnMXKXfae)</li>
  <li><b>model.npz</b> (https://drive.google.com/file/d/1ZA3jEKcVCKqOXWWfeQiyFKAf6U35Fk1H/view?fbclid=IwAR3VSVWOihGIC0AG1NAFdy_COgOTiNCgL7DX73HyANbMWCy7J_dFQnWXZ4Q)</li>
  <li><b>chatbotDatabase.db</b> (https://drive.google.com/file/d/1HzGQO5L1RaDz0ezFB0_tYLsfZZ8ssq1X/view?fbclid=IwAR1OigHNMzG6ALOYojC0NixrLDjrhIwoCb5P3ZOK4Z3OGSbbgTcAmzmzkro)</li>
</ul>


Da biste pokrenuli aplikaciju i samostalno testirali model koji smo trenirale, potrebno je pokrenuti fajl <b>main.py</b>. Tada putem konzole možete prosleđivati rečenice i aplikacija će izbacivati odgovore na njih.

Radi lakše i brže provere, možete pokrenuti i fajl <b>check_sentences.py</b>. U ovom slučaju, u aplikaciji se prosleđuju pitanja koja smo mi izdvojile i prikazuju se zajedno sa izbačenim odgovorom.


## Postupak pripreme dataseta
U daljem tekstu ćemo detaljno objasniti postupak po kom smo dataset pripremile za treniranje i koji bi se mogao ponoviti u slučaju kreiranja novog dataseta.

### 1. Pokretanje read_data.py
Pokretanjem ovog fajla želimo da iz prvobitnog dataset-a izdvojimo samo one podatke koji su nam potrebni za obučavanje naše mreže. Naš prvobitni dataset predstavlja fajl <b>RC_2013-06</b>, koji sadrži sve komentare ostavljene na Reddit-u juna 2013. godine, zadate u JSON formatu. Uz određene kriterijume, iz ovog JSON fajla smo izdvojile komentare i njihove "najbolje" podkomentare i smestile ih u bazu podataka, odnosno u <b>databaseChatbot.db</b>. Ovaj korak nama je trajao nekoliko sati.

### 2. Pokretanje generate_to_from.py

Nakon pokretanja ovog fajla, podaci iz <b>databaseChatbot.db</b> se smeštaju u dva nova fajla: <b>from.txt</b> i <b>to.txt</b>. Prvi fajl sadrži input rečenice, a drugi odgovarajuće output-e ili odgovore na rečenice iz prvog fajla. Svaka linija u <b>from.txt</b> fajlu odgovara istoj liniji u <b>to.txt</b> fajlu.

### 3. Pokretanje filter_data.py

U ovom koraku se iz <b>from.txt</b> i <b>to.txt</b> filtriraju sve rečenice, reči i simboli koji nisu odgovarajući za treniranje naše mreže. Kao rezultat pokretanja ovog fajla generišu se <b>train_from_filtered</b> i <b>train_to_filtered</b>.

### 4. Pokretanje correct_data.py

U ovom koraku se uz pomoć NLTK biblioteke koriguju neke od nepravilno napisanih reči kako ne bi stvarale teškoće prilikom obučavanja mreže. Kao rezultat pokretanja ovog fajla generišu se <b>train_from_corrected</b> i <b>train_to_corrected</b>.

### 5. Pokretanje generate_metadata.py

Pokretanjem ovog fajla, generiše se <b>metadataFirst.pkl</b>, koji sadrži sve input rečenice iz dataseta i odgovarajuće outpute. Svaki input i output je predstavljen nizom brojeva, a svakom broju odgovara jedna reč. Takođe ovaj fajl sadrži tokenizer koji sadrži informaciju o vezi između brojeva i reči u vidu rečnika, kao i odgovarajuće metode za konverziju reči u brojeve i obrnuto. Ovaj fajl će se koristiti pri treningu i pri kasnijem korišćenju obučene mreže.


## Treniranje neuronske mreže
Nakon što je dataset kompletno pripremljen, može se preći na korak obučavanja mreže. Da bi se obučavanje mreže pokrenulo, potrebno je pokrenuti <b>train.py</b>. 
