# SST - Zadanie z sygnałem STOP

## Uruchamianie

```
python main.py config/config.yaml
```

## Przygotowanie eksperymentu

<pre>
Aby przygotowac eksperyment wykonaj pokolei następujące kroki:
1) Bodźce
    * Wszystkie bodźce go i stop należy wgrać do odpowiednich folderów (patrz "Struktura procedury")
2) Config
    * Config jest ustalany raz przed cała sesją eksperymentalną i nie powinien byc zmieniany w jej trakcie.
    * Ustawianie configu odbywa sie w dwóch krokach (pierwszy można pominąć, ale ułatwia on konfigurację):
        a) Uruchomienie programu "edit_config.py"
        -------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!------------------------------
        b) Edycja pliku "congig.yaml" z folderu "config"
        ---------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!----------------------------
3) Uruchamianie
    * Gdy mamy poprawnie przygotowana procedurę dla każdej osoby badanej wystarczy uruchomic program "run.py"
    * Po uruchomieniu wyświetli sie okienko, w którym trzeba wpisać:
        @ ID - ID osoby badanej (według zasad ustalonych w laboratorium)
        @ Age - wiek osoby badanej
        @ Sex - płeć osoby badanej
        @ Observer - w tym miejscu można wpisać nazwę osoby przeprowadzającej badania (jeżeli inna niz w configu
    * Gdy wpiszemy powyższe dane i nacisniemy przycisk OK procedura się uruchomi.
    * Procedure można wyłączyć w dowolnej chwili klawiszem "F7".
    <font color="red">* UWAGA: dane zapisują się tylko i wyłącznie na koniec procedury. Jeżeli z jakiegokolwiek powodu procedura zostanie przerwana wszystkie dane zostana utracone!</font>
</pre>

## Struktura procedury

<pre>
Procedura zawiera nastepujące foldery:
1) arrows
    * Zawiera pliki z bodźcami GO.
    * Dostępne formaty plików:
        - zdjęcia - 'bmp', 'jpg', 'png'
        - pliki audio - 'mp3', 'au', 'mp2', 'wav', 'wma', 'ogg'
        - pliki tekstowe - 'txt'.
    * Nazwenictwo bodźców:
        - Bodźce moga być podzielone na grupy tematyczne. Jeżeli nazwa pliku zawiera '_' ciag znaków przed tym symbolem będzie traktowany jako nazwa grupy, 
          a po nim jako nazwa konkretnego bodźca. Jeżeli plik nie zawiera '_' to jego nazwa jest zarówno grupa jak i indywidualna nazwą. Domyslnie na bodźce
          z jednej grupy reaguje sie tym samym klawiszem.
        - Pliki tekstowe są wyjatkiem. Nazwa pliku nie ma znaczenia. W pliku może znajdować się dowolna liczba bodźców. Każdy bodziec znajduje sie w osobnej
          linijce i ma postać "nazwagrupy_nazwabodźca:tekst do wyswietlenia".
        - Przykład:
            @ W folderze arrow znajdują sie nastepujace pliki 'dog_1v.mp3, cat_2v.mp3, dog_1i.jpg, cat_2i.jpg, arrows.txt'.
            @ W pliku 'arrows.txt' znajduje się jeden bodzic 'dog_1t:hau hau'.
            @ Mamy zatem 5 bodźców (1v, 2v, 1i, 2i, 1t) i dwie grupy (dog, cat).
            @ Badany bęzie zatem uzywał dwóch klawiszy jeden do reagowania na bodźce 'dog', drugi do reagowania na bodxce 'cat'.

2) classes
    * Zawiera pliki z kodem napisanym w pythonie (Psychopy 1.82.01)

3) config
    * zawiera plik 'config.yaml', w którym można ustawić wszystkie konfiguracje procedury (patrz rozdział config).
    
4) messages
    * zawiera nastepujące pliki:
        - 'answers_correctness.txt' - zawiera tekst, który ma się wyswietlić jeżeli chcemy w przerwach umieszczać informację o procencie poprawnych odpowiedzi.
                                      W pliku musi znaleść sie linika o tresci "<--insert-->" - w tym miejscu program wstawi obliczony wynik.
        - 'break*.txt' - zawiera tekst, który ma się wyświetlić po konkretnym bloku procedury. W miejsce '*' nalezy wstawić konkretna liczbę. W pliku musi znaleść 
                         się linika o tresci "<--insert-->" - w tym miejscu program wyświtli dodatkowe informacje (patrz rozdział config).
        - 'end.txt' - zawiera tekst, który ma się wyświetlić na końcu procedury.
        - 'instruction.txt', 'instruction*.txt' - pliki z instrukcja wyświtlana na samym poczatku procedury. Jako pierwszy wyswietli się tekst w pliku 'instruction.txt'
                                                  nastepnie wyświetlane będa pliki 'instruction*.txt', gdzie pod * podstawiane sa kolejne numery poczynajac od 1.
                                                  Plików z instrukcjami może być dowolna liczba.
        - 'ophthalmic_corners.txt' - informacja, która wyswietli sie przed procedura oczną (ruch gałek ocznych).
        - 'ophthalmic_instruction.txt' - informacja, która wyswietli sie przed procedura oczną (mruganie oczami).
        - 'response_time.txt' - zawiera tekst, który ma się wyswietlić jeżeli chcemy w przerwach umieszczać informację o srednim czasie reakcji.
                                W pliku musi znaleść sie linika o tresci "<--insert-->" - w tym miejscu program wstawi obliczony wynik.
        - 'stopped_ratio.txt' - zawiera tekst, który ma się wyswietlić jeżeli chcemy w przerwach umieszczać informację o procencie wyhamowanych odpowiedzi.
                                W pliku musi znaleść sie linika o tresci "<--insert-->" - w tym miejscu program wstawi obliczony wynik.
        - 'training_end.txt' - zawiera tekst, który ma się wyświetlić na końcu treningu.

5) results
    * zawiera dwa foldery
        - 'behavioral_data'
            @ ----!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!---------
        - 'triggers_maps'
            @ Zawiera pliki, które są mapowaniami triggerów dla programów do obróbki sygnału.
            @ Nazwy plików są formatu "triggerMap_id.txt", gdzie 'id" jest nazwa konkretnej osoby badanej.
            @ W każdej linijce pliku znajduje sie jeden trigger.
            @ Linika w pliku ma nastepujacom budowe "numertriggeru:nazwatriggeru".
            @ Triggery są numerowane w pętlach i mają numery od 1 do 8.
            @ Nazwa triggeru ma nastepująca budowę "typ_wydarzenia*typ_bodźca*nazwa_bodźca*typ_bodźca_stop*nazwa_bodźca_stop*czas_oczekiwania_na_stop*reakcja".
                > typ_wydarzenia - "GO" - bodziec go, "ST" - bodziec stop, "RE" - reakcja osoby badanej
                > typ_bodźca - image, text, sound
                > nazwa_bodźca - nazwagrupy_nazwabodźca
                > typ_bodźca_stop - jeżeli stop występuje w trialu patrz typ_wydarzenia, jeżeli stop nie wystepuje "-"
                > nazwa_bodźca_stop - jeżeli stop występuje w trialu patrz nazwa_bodźca, jeżeli stop nie wystepuje "-"
                > czas_oczekiwania_na_stop - jeżeli stop występuje w trialu w tym miejscu pojawi się czas oczekiwania na stop od momentu wyświetlenia się bodźca GO, 
                  jeżeli stop nie wystepuje "-".
                > reakcja - klawisz, który nacisnął badany.
6) stops
    * Zawiera pliki z bodźcami stop.
    * Analogicznie do folderu arrows.
</pre>