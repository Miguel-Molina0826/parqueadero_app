package app.parqueadero;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;
import java.net.URL;

/**
 * Clase principal de la aplicación Parqueadero.
 * Extiende de Application para inicializar y cargar la vista FXML y los estilos CSS.
 */
public class Main extends Application {

    @Override
    public void start(Stage stage) throws IOException {
        // Carga de la vista FXML
        URL fxmlLocation = getClass().getResource("parqueadero-view.fxml");
        if (fxmlLocation == null) {
            throw new IllegalStateException("No se encontró el archivo FXML: parqueadero-view.fxml");
        }
        FXMLLoader fxmlLoader = new FXMLLoader(fxmlLocation);
        Scene scene = new Scene(fxmlLoader.load(), 1080, 720);

        // Carga explícita de la hoja de estilos CSS
        URL cssLocation = getClass().getResource("styles.css");
        if (cssLocation != null) {
            scene.getStylesheets().add(cssLocation.toExternalForm());
        }

        stage.setTitle("Sistema de Gestión de Parqueadero - Control de Acceso");
        stage.setMinWidth(920);
        stage.setMinHeight(620);
        stage.setScene(scene);
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
