import automata.Automaton;
import automata.AutomatonSimulator;
import automata.SimulatorFactory;
import java.io.File;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

/** Corre los casos (archivo TAB cadena) en el motor de JFLAP y escribe el veredicto. */
public class JflapLote {
    public static void main(String[] args) throws Exception {
        try (PrintWriter salida = new PrintWriter(args[1], "UTF-8")) {
            for (String linea : Files.readAllLines(Paths.get(args[0]), StandardCharsets.UTF_8)) {
                String[] p = linea.split("\t", -1);
                Automaton a = (Automaton) new file.XMLCodec().decode(new File(p[0]), null);
                AutomatonSimulator s = SimulatorFactory.getSimulator(a);
                salida.println(p[0] + "\t" + p[1] + "\t" + s.simulateInput(p[1]));
            }
        }
        System.exit(0);
    }
}
