# Basketball Checker

## Beschreibung

Basketball Checker ist ein Brettspiel für den Computer. Das Spiel ist eine Mischung aus Dame auch bekannt als Checker und Basketball. Zwei Teams spielen gegeneinander: Schwarz und Weiss. Jedes Team hat Figuren und einen Korb. Das Spielfeld hat 11 Reihen und 9 Spalten.

## Abhängigkeiten

- Python 3.13 oder höher
- pygame-ce 2.5.8

Die Datei requirements.txt enthält alle Python-Pakete.

## Installation

HINWEIS: Installieren Sie nicht pygame und pygame-ce zusammen. Beide Pakete verwenden das gleiche Modul pygame.

1. Installieren Sie Python 3.13 oder höher.
2. Öffnen Sie ein Terminal im Projektordner.
3. Installieren Sie die Pakete:

   ```
   pip install -r requirements.txt
   ```

## Spiel starten

1. Öffnen Sie ein Terminal im Projektordner.
2. Starten Sie das Programm:

   ```
   python main.py
   ```

3. Geben Sie im Terminal einen Modus ein.
4. Drücken Sie Enter.

Das Spielfenster wird sich öffnen.

Modi:

- `bot` oder `b`: Sie spielen gegen den Computer. Sie spielen mit Weiss.
- `1v1`, `1` oder `v`: Zwei Personen spielen an einem Computer.
- `simulation` oder `s`: Der Computer spielt gegen sich selbst.

## Bedienung

Die Figuren des aktiven Teams haben einen orangen Rand. Der Ball ist ein oranger Kreis in einer Figur. Der Korb ist eine Figur mit einem orangen Ring. Oben im Fenster steht die Spielzeit.

1. Klicken Sie auf eine Figur des aktiven Teams. Die möglichen Felder sind dann heller.
2. Klicken Sie auf ein helles Feld. Die Figur bewegt sich auf dieses Feld.

Um eine andere Figur zu wählen, klicken Sie auf diese Figur.

Um das Spiel zu beenden, schliessen Sie das Fenster.

## Regeln

- Am Start bekommt eine zufällige Figur den Ball. Das Team dieser Figur beginnt.
- Im Modus bot bekommt immer eine weisse Figur den Ball.
- Eine Figur bewegt sich diagonal ein Feld nach vorne.
- Am Ende des Spielfelds ändert die Figur die Richtung.
- Eine Figur kann diagonal über eine Figur des anderen Teams springen. Das Feld hinter dieser Figur muss frei sein.
- Die übersprungene Figur ist dann aus dem Spiel. Wenn diese Figur den Ball hat, bekommt Ihre Figur den Ball.
- Die Figur mit dem Ball kann den Ball passen. Das Ziel ist eine Figur des gleichen Teams in der gleichen Reihe oder Spalte. Zwischen den zwei Figuren darf keine andere Figur sein.
- Ein Team gewinnt, wenn die Figur mit dem Ball über den Korb des anderen Teams springt.

Zeitlimit beim Korb:

- Die vier Felder diagonal neben einem Korb haben ein Zeitlimit.
- Bei jedem Zug ihres Teams steigt der Zähler einer Figur auf diesen Feldern um 1.
- Ein farbiger Punkt auf der Figur zeigt den Zähler: gelb bei 1, hellrot bei 2, rot bei 3.
- Bei 4 ist die Figur aus dem Spiel. Wenn diese Figur den Ball hat, bekommt das andere Team den Ball.
- Der Zähler geht auf 0, wenn die Figur diese Felder verlässt.

## Spielende

Am Ende ist der Hintergrund orange. Das Fenster zeigt die Spielzeit und das Gewinner-Team. Das Fenster schliesst nach 20 Sekunden automatisch.

## Hinweis zu den Dateien

- Zur Ausführung muss man nur main.py starten. Dsas ganze Spiel funktioniert mit den Dateien main.py, board.py sowie Piece.py. 
- Die Datei old_board.py diente nur dem Entwickler(mir, Djordje) um die Spiellogik anzupassen mit einem Vergleich an seiner Seite.