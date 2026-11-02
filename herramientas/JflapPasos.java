import java.awt.Component;
import java.awt.Container;
import java.awt.Graphics2D;
import java.awt.Window;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.Serializable;
import javax.imageio.ImageIO;
import javax.swing.AbstractButton;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;

/** Abre un .jff en la ventana real de JFLAP, simula paso a paso y guarda cada paso. */
public class JflapPasos {
    static AbstractButton buscar(Container c, String texto) {
        for (Component h : c.getComponents()) {
            if (h instanceof AbstractButton && texto.equals(((AbstractButton) h).getText())) return (AbstractButton) h;
            if (h instanceof Container) {
                AbstractButton r = buscar((Container) h, texto);
                if (r != null) return r;
            }
        }
        return null;
    }

    static JTextField campo(Container c) {
        for (Component h : c.getComponents()) {
            if (h instanceof JTextField) return (JTextField) h;
            if (h instanceof Container) {
                JTextField r = campo((Container) h);
                if (r != null) return r;
            }
        }
        return null;
    }

    static void pulsar(AbstractButton b) throws Exception {
        SwingUtilities.invokeAndWait(b::doClick);
    }

    static void foto(JFrame f, File destino) throws Exception {
        BufferedImage i = new BufferedImage(f.getWidth(), f.getHeight(), BufferedImage.TYPE_INT_RGB);
        SwingUtilities.invokeAndWait(() -> { Graphics2D g = i.createGraphics(); f.printAll(g); g.dispose(); });
        ImageIO.write(i, "png", destino);
    }

    public static void main(String[] a) throws Exception {
        Object aut = new file.XMLCodec().decode(new File(a[0]), null);
        JFrame[] marco = new JFrame[1];
        SwingUtilities.invokeAndWait(gui.action.NewAction::showNew);
        SwingUtilities.invokeAndWait(() -> marco[0] = gui.environment.FrameFactory.createFrame((Serializable) aut));
        JFrame f = marco[0];
        Thread.sleep(800);
        JMenuItem opcion = null;
        for (int m = 0; m < f.getJMenuBar().getMenuCount(); m++) {
            JMenu menu = f.getJMenuBar().getMenu(m);
            for (int k = 0; menu != null && k < menu.getItemCount(); k++) {
                JMenuItem it = menu.getItem(k);
                if (it != null && it.getText() != null && it.getText().startsWith("Step with Closure")) opcion = it;
            }
        }
        final JMenuItem elegido = opcion;
        SwingUtilities.invokeLater(elegido::doClick);
        Thread.sleep(800);
        for (Window w : Window.getWindows()) {
            if (w.isVisible() && w != f && w instanceof Container && campo((Container) w) != null) {
                JTextField t = campo((Container) w);
                SwingUtilities.invokeAndWait(() -> t.setText(a[1]));
                pulsar(buscar((Container) w, "OK"));
            }
        }
        Thread.sleep(800);
        f.setSize(1000, 620);
        f.validate();
        Thread.sleep(400);
        foto(f, new File(a[2] + "-paso0.png"));
        AbstractButton paso = buscar(f.getContentPane(), "Step");
        for (int i = 1; i <= a[1].length(); i++) {
            pulsar(paso);
            Thread.sleep(300);
            foto(f, new File(a[2] + "-paso" + i + ".png"));
        }
        System.exit(0);
    }
}
