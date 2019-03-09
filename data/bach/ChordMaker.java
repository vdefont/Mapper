import java.util.*;
import java.io.*;

class ChordMaker {

  private static final String START = "SONG_START", END = "SONG_END";

  Map<String,Map<String,Integer>> bigramFreq;
  Map<String,Integer> counts;

  public ChordMaker () {
    bigramFreq = new HashMap<>();
    counts = new HashMap<>();
    readFile();
    printMaps();

    // Make a song
    List<String> song = generateSong();
    for (String chord : song) {
      System.out.println(chord);
    }
    System.out.println("SONG LENGTH: " + song.size());
  }

  private void printMaps () {

    // Print bigram map
    for (String k : bigramFreq.keySet()) {
      if (k.equals("A#d")) {
        System.out.println(k);
        for (String k2 : bigramFreq.get(k).keySet()) {
          int freq = bigramFreq.get(k).get(k2);
          System.out.println("  " + k2 + " --- " + freq);
        }
      }
    }

    // Print count map
    // for (String k : counts.keySet()) {
    //   int count = counts.get(k);
    //   System.out.println(k + " --- " + count);
    // }
  }

  private void addToMaps (String chordA, String chordB) {

    // Ensure keys exist
    if (!bigramFreq.containsKey(chordA)) {
      bigramFreq.put(chordA, new HashMap<>());
    }
    if (!bigramFreq.get(chordA).containsKey(chordB)) {
      bigramFreq.get(chordA).put(chordB, 0);
    }
    if (!counts.containsKey(chordA)) {
      counts.put(chordA, 0);
    }

    // Add to maps
    int curFreq = bigramFreq.get(chordA).get(chordB);
    int curCount = counts.get(chordA);
    bigramFreq.get(chordA).put(chordB, curFreq + 1);
    counts.put(chordA, curCount + 1);

  }

  private void readFile () {
    try (BufferedReader br = new BufferedReader(new FileReader("chords.csv"))) {
      String line;

      String prevSongId = "";
      String prevChord = START;
      while ((line = br.readLine()) != null) {
        String[] fields = line.split(",");
        String songId = fields[0];
        String chord = fields[16];
        if (prevSongId.equals("") || songId.equals(prevSongId)) {
          addToMaps(prevChord, chord);
        }
        // If we're moving on to a new song
        else {
          addToMaps(prevChord, END);
          addToMaps(START, chord);
        }
        prevSongId = songId;
        prevChord = chord;
      }
      addToMaps(prevChord, END);
    } catch (IOException e) {
      System.out.println("Error reading file: " + e);
    }
  }

  private String randomNextChord (String chord) {
    int count = counts.get(chord);
    int chordIndex = (int) (Math.random() * count);
    int cumSum = 0;
    for (String nextChord : bigramFreq.get(chord).keySet()) {
      cumSum += bigramFreq.get(chord).get(nextChord);
      if (cumSum > chordIndex) return nextChord;
    }
    return "";
  }

  private List<String> generateSong () {
    String prevChord = START;
    List<String> chords = new ArrayList<>();
    while (!prevChord.equals(END)) {
      String chord = randomNextChord(prevChord);
      chords.add(chord);
      prevChord = chord;
    }
    return chords;
  }

  public static void main (String[] args) {
    new ChordMaker();
  }

}
