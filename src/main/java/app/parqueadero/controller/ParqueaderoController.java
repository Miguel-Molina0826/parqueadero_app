package app.parqueadero.controller;

import app.parqueadero.model.Vehiculo;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.collections.transformation.SortedList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;

import java.net.URL;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Optional;
import java.util.ResourceBundle;

/**
 * Controlador de la vista principal del sistema de gestión de parqueadero.
 * Gestiona el CRUD en memoria a través de un ArrayList<Vehiculo> sincronizado con la TableView.
 */
public class ParqueaderoController implements Initializable {

    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    // Campos del formulario lateral
    @FXML private TextField txtPlaca;
    @FXML private ComboBox<String> cbTipoVehiculo;
    @FXML private TextField txtPropietario;
    @FXML private TextField txtHoraIngreso;

    // Botones de acción CRUD
    @FXML private Button btnRegistrar;
    @FXML private Button btnActualizar;
    @FXML private Button btnEliminar;
    @FXML private Button btnLimpiar;

    // Búsqueda y tabla
    @FXML private TextField txtBuscar;
    @FXML private TableView<Vehiculo> tblVehiculos;
    @FXML private TableColumn<Vehiculo, String> colPlaca;
    @FXML private TableColumn<Vehiculo, String> colTipoVehiculo;
    @FXML private TableColumn<Vehiculo, String> colPropietario;
    @FXML private TableColumn<Vehiculo, String> colHoraIngreso;

    // Estadísticas y estado
    @FXML private Label lblTotalVehiculos;
    @FXML private Label lblEstado;

    // 1. Estructura de almacenamiento en memoria requerida (ArrayList)
    private final ArrayList<Vehiculo> listaVehiculos = new ArrayList<>();

    // 2. Colección observable vinculada a la UI de JavaFX
    private final ObservableList<Vehiculo> observableVehiculos = FXCollections.observableArrayList();
    private FilteredList<Vehiculo> listaFiltrada;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        configurarComboTipos();
        configurarColumnasTabla();
        configurarEventosSeleccion();
        cargarDatosDePrueba();
        listarVehiculos();
        configurarFiltroBusqueda();
        limpiarFormulario();
    }

    private void configurarComboTipos() {
        cbTipoVehiculo.setItems(FXCollections.observableArrayList(
                "Automóvil",
                "Motocicleta",
                "Camioneta",
                "Bicicleta",
                "Vehículo Pesado"
        ));
        cbTipoVehiculo.getSelectionModel().selectFirst();
    }

    private void configurarColumnasTabla() {
        colPlaca.setCellValueFactory(new PropertyValueFactory<>("placa"));
        colTipoVehiculo.setCellValueFactory(new PropertyValueFactory<>("tipoVehiculo"));
        colPropietario.setCellValueFactory(new PropertyValueFactory<>("propietario"));
        colHoraIngreso.setCellValueFactory(new PropertyValueFactory<>("horaIngreso"));

        tblVehiculos.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);
    }

    private void configurarEventosSeleccion() {
        tblVehiculos.getSelectionModel().selectedItemProperty().addListener((obs, anterior, seleccionado) -> {
            if (seleccionado != null) {
                cargarVehiculoEnFormulario(seleccionado);
            }
        });
    }

    private void configurarFiltroBusqueda() {
        listaFiltrada = new FilteredList<>(observableVehiculos, p -> true);

        txtBuscar.textProperty().addListener((observable, oldValue, newValue) -> {
            listaFiltrada.setPredicate(vehiculo -> {
                if (newValue == null || newValue.isBlank()) {
                    return true;
                }

                String termino = newValue.toLowerCase().trim();
                return vehiculo.getPlaca().toLowerCase().contains(termino)
                        || vehiculo.getPropietario().toLowerCase().contains(termino)
                        || vehiculo.getTipoVehiculo().toLowerCase().contains(termino);
            });
            actualizarContadores();
        });

        SortedList<Vehiculo> datosOrdenados = new SortedList<>(listaFiltrada);
        datosOrdenados.comparatorProperty().bind(tblVehiculos.comparatorProperty());
        tblVehiculos.setItems(datosOrdenados);
    }

    /**
     * Datos iniciales precargados en el ArrayList para demostración.
     */
    private void cargarDatosDePrueba() {
        listaVehiculos.add(new Vehiculo("ABC-123", "Automóvil", "Carlos Mendoza", LocalDateTime.now().minusHours(2).format(FORMATTER)));
        listaVehiculos.add(new Vehiculo("MTO-45B", "Motocicleta", "Andrea Suárez", LocalDateTime.now().minusHours(1).minusMinutes(15).format(FORMATTER)));
        listaVehiculos.add(new Vehiculo("KLO-987", "Camioneta", "Fernando Torres", LocalDateTime.now().minusMinutes(35).format(FORMATTER)));
    }

    /**
     * CRUD: Listar (Leer)
     * Sincroniza la lista observable de la tabla con los datos del ArrayList<Vehiculo>.
     */
    public void listarVehiculos() {
        observableVehiculos.setAll(listaVehiculos);
        actualizarContadores();
    }

    private void cargarVehiculoEnFormulario(Vehiculo v) {
        txtPlaca.setText(v.getPlaca());
        txtPlaca.setDisable(true); // Bloquear placa como clave primaria de búsqueda
        cbTipoVehiculo.setValue(v.getTipoVehiculo());
        txtPropietario.setText(v.getPropietario());
        txtHoraIngreso.setText(v.getHoraIngreso());

        btnRegistrar.setDisable(true);
        btnActualizar.setDisable(false);
        btnEliminar.setDisable(false);

        lblEstado.setText("Vehículo seleccionado: " + v.getPlaca());
    }

    /**
     * CRUD: Registrar (Crear)
     * Valida y agrega un nuevo vehículo al ArrayList<Vehiculo>.
     */
    @FXML
    public void onRegistrar() {
        String placa = txtPlaca.getText().trim().toUpperCase();
        String tipo = cbTipoVehiculo.getValue();
        String propietario = txtPropietario.getText().trim();
        String hora = txtHoraIngreso.getText().trim();

        // Validaciones de datos obligatorios
        if (placa.isEmpty() || propietario.isEmpty()) {
            mostrarAlerta(Alert.AlertType.WARNING, "Campos Incompletos", "Debe ingresar tanto la placa como el nombre del propietario.");
            return;
        }

        if (tipo == null || tipo.isBlank()) {
            mostrarAlerta(Alert.AlertType.WARNING, "Campos Incompletos", "Seleccione un tipo de vehículo.");
            return;
        }

        // Validación de no duplicidad de placa en el ArrayList
        boolean existe = listaVehiculos.stream().anyMatch(v -> v.getPlaca().equalsIgnoreCase(placa));
        if (existe) {
            mostrarAlerta(Alert.AlertType.ERROR, "Vehículo Duplicado", "Ya existe un vehículo registrado con la placa " + placa + ".");
            return;
        }

        if (hora.isEmpty()) {
            hora = LocalDateTime.now().format(FORMATTER);
        }

        Vehiculo nuevoVehiculo = new Vehiculo(placa, tipo, propietario, hora);
        listaVehiculos.add(nuevoVehiculo);

        listarVehiculos();
        limpiarFormulario();
        lblEstado.setText("Vehículo " + placa + " registrado exitosamente.");
        mostrarAlerta(Alert.AlertType.INFORMATION, "Registro Exitoso", "El vehículo " + placa + " ingresó al parqueadero.");
    }

    /**
     * CRUD: Actualizar
     * Modifica los datos del vehículo seleccionado en el ArrayList<Vehiculo>.
     */
    @FXML
    public void onActualizar() {
        Vehiculo seleccionado = tblVehiculos.getSelectionModel().getSelectedItem();
        if (seleccionado == null) {
            mostrarAlerta(Alert.AlertType.WARNING, "Selección Requerida", "Seleccione un vehículo de la tabla para actualizar.");
            return;
        }

        String propietario = txtPropietario.getText().trim();
        String tipo = cbTipoVehiculo.getValue();
        String hora = txtHoraIngreso.getText().trim();

        if (propietario.isEmpty()) {
            mostrarAlerta(Alert.AlertType.WARNING, "Campos Incompletos", "El nombre del propietario no puede quedar vacío.");
            return;
        }

        // Actualizar en el objeto perteneciente al ArrayList
        seleccionado.setTipoVehiculo(tipo);
        seleccionado.setPropietario(propietario);
        if (!hora.isEmpty()) {
            seleccionado.setHoraIngreso(hora);
        }

        listarVehiculos();
        tblVehiculos.refresh();
        lblEstado.setText("Vehículo " + seleccionado.getPlaca() + " actualizado.");
        mostrarAlerta(Alert.AlertType.INFORMATION, "Actualización Exitosa", "Los datos del vehículo han sido modificados.");
    }

    /**
     * CRUD: Eliminar (Registrar Salida)
     * Remueve el vehículo del ArrayList<Vehiculo> tras confirmación.
     */
    @FXML
    public void onEliminar() {
        Vehiculo seleccionado = tblVehiculos.getSelectionModel().getSelectedItem();
        if (seleccionado == null) {
            mostrarAlerta(Alert.AlertType.WARNING, "Selección Requerida", "Seleccione un vehículo de la tabla para registrar salida.");
            return;
        }

        Alert confirmacion = new Alert(Alert.AlertType.CONFIRMATION);
        confirmacion.setTitle("Confirmar Salida/Eliminación");
        confirmacion.setHeaderText("¿Desea registrar la salida del vehículo " + seleccionado.getPlaca() + "?");
        confirmacion.setContentText("Esta acción eliminará el vehículo del registro actual del parqueadero.");

        Optional<ButtonType> resultado = confirmacion.showAndWait();
        if (resultado.isPresent() && resultado.get() == ButtonType.OK) {
            listaVehiculos.remove(seleccionado);
            listarVehiculos();
            limpiarFormulario();
            lblEstado.setText("Vehículo " + seleccionado.getPlaca() + " retirado del parqueadero.");
        }
    }

    /**
     * Limpia los campos del formulario y deselecciona la tabla.
     */
    @FXML
    public void onLimpiar() {
        limpiarFormulario();
    }

    private void limpiarFormulario() {
        txtPlaca.clear();
        txtPlaca.setDisable(false);
        txtPropietario.clear();
        txtHoraIngreso.setText(LocalDateTime.now().format(FORMATTER));
        if (cbTipoVehiculo.getItems() != null && !cbTipoVehiculo.getItems().isEmpty()) {
            cbTipoVehiculo.getSelectionModel().selectFirst();
        }

        tblVehiculos.getSelectionModel().clearSelection();

        btnRegistrar.setDisable(false);
        btnActualizar.setDisable(true);
        btnEliminar.setDisable(true);

        lblEstado.setText("Listo para nuevo registro.");
    }

    private void actualizarContadores() {
        int total = listaVehiculos.size();
        int filtrados = (listaFiltrada != null) ? listaFiltrada.size() : total;

        if (txtBuscar != null && !txtBuscar.getText().isBlank()) {
            lblTotalVehiculos.setText(String.format("Mostrando: %d de %d", filtrados, total));
        } else {
            lblTotalVehiculos.setText(String.format("Total en Parqueadero: %d", total));
        }
    }

    private void mostrarAlerta(Alert.AlertType tipo, String titulo, String mensaje) {
        Alert alerta = new Alert(tipo);
        alerta.setTitle(titulo);
        alerta.setHeaderText(null);
        alerta.setContentText(mensaje);
        alerta.showAndWait();
    }
}
