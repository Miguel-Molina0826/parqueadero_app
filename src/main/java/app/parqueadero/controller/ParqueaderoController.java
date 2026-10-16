package app.parqueadero.controller;

import app.parqueadero.model.Vehiculo;
<<<<<<< HEAD
import javafx.beans.property.SimpleStringProperty;
=======
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2
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
<<<<<<< HEAD
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.Locale;
=======
import java.util.ArrayList;
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2
import java.util.Optional;
import java.util.ResourceBundle;

/**
 * Controlador de la vista principal del sistema de gestión de parqueadero.
<<<<<<< HEAD
 * Gestiona el CRUD en memoria a través de un ArrayList<Vehiculo> sincronizado con la TableView,
 * así como la liquidación y cobro por horas de estacionamiento al momento de la salida.
=======
 * Gestiona el CRUD en memoria a través de un ArrayList<Vehiculo> sincronizado con la TableView.
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2
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
<<<<<<< HEAD
        colHoraIngreso.setCellValueFactory(cellData -> {
            Vehiculo v = cellData.getValue();
            return new SimpleStringProperty(v != null ? v.getHoraIngresoFormateada() : "");
        });
=======
        colHoraIngreso.setCellValueFactory(new PropertyValueFactory<>("horaIngreso"));
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2

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
<<<<<<< HEAD
     * Datos iniciales precargados en el ArrayList con diferentes rangos de tiempo para demostración.
     */
    private void cargarDatosDePrueba() {
        listaVehiculos.add(new Vehiculo("ABC-123", "Automóvil", "Carlos Mendoza", LocalDateTime.now().minusHours(2)));
        listaVehiculos.add(new Vehiculo("MTO-45B", "Motocicleta", "Andrea Suárez", LocalDateTime.now().minusHours(1).minusMinutes(15)));
        listaVehiculos.add(new Vehiculo("KLO-987", "Camioneta", "Fernando Torres", LocalDateTime.now().minusMinutes(35)));
=======
     * Datos iniciales precargados en el ArrayList para demostración.
     */
    private void cargarDatosDePrueba() {
        listaVehiculos.add(new Vehiculo("ABC-123", "Automóvil", "Carlos Mendoza", LocalDateTime.now().minusHours(2).format(FORMATTER)));
        listaVehiculos.add(new Vehiculo("MTO-45B", "Motocicleta", "Andrea Suárez", LocalDateTime.now().minusHours(1).minusMinutes(15).format(FORMATTER)));
        listaVehiculos.add(new Vehiculo("KLO-987", "Camioneta", "Fernando Torres", LocalDateTime.now().minusMinutes(35).format(FORMATTER)));
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2
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
<<<<<<< HEAD
        txtHoraIngreso.setText(v.getHoraIngresoFormateada());
=======
        txtHoraIngreso.setText(v.getHoraIngreso());
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2

        btnRegistrar.setDisable(true);
        btnActualizar.setDisable(false);
        btnEliminar.setDisable(false);

        lblEstado.setText("Vehículo seleccionado: " + v.getPlaca());
    }

    /**
     * CRUD: Registrar (Crear)
<<<<<<< HEAD
     * Valida y agrega un nuevo vehículo al ArrayList<Vehiculo> con su fecha y hora en LocalDateTime.
=======
     * Valida y agrega un nuevo vehículo al ArrayList<Vehiculo>.
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2
     */
    @FXML
    public void onRegistrar() {
        String placa = txtPlaca.getText().trim().toUpperCase();
        String tipo = cbTipoVehiculo.getValue();
        String propietario = txtPropietario.getText().trim();
<<<<<<< HEAD
        String horaTexto = txtHoraIngreso.getText().trim();
=======
        String hora = txtHoraIngreso.getText().trim();
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2

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

<<<<<<< HEAD
        LocalDateTime horaIngreso;
        if (horaTexto.isEmpty()) {
            horaIngreso = LocalDateTime.now();
        } else {
            try {
                horaIngreso = LocalDateTime.parse(horaTexto, FORMATTER);
            } catch (DateTimeParseException e) {
                mostrarAlerta(Alert.AlertType.WARNING, "Formato Inválido", "La hora de ingreso debe tener el formato: yyyy-MM-dd HH:mm:ss");
                return;
            }
        }

        Vehiculo nuevoVehiculo = new Vehiculo(placa, tipo, propietario, horaIngreso);
=======
        if (hora.isEmpty()) {
            hora = LocalDateTime.now().format(FORMATTER);
        }

        Vehiculo nuevoVehiculo = new Vehiculo(placa, tipo, propietario, hora);
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2
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
<<<<<<< HEAD
        String horaTexto = txtHoraIngreso.getText().trim();
=======
        String hora = txtHoraIngreso.getText().trim();
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2

        if (propietario.isEmpty()) {
            mostrarAlerta(Alert.AlertType.WARNING, "Campos Incompletos", "El nombre del propietario no puede quedar vacío.");
            return;
        }

<<<<<<< HEAD
        LocalDateTime horaIngreso = seleccionado.getHoraIngreso();
        if (!horaTexto.isEmpty()) {
            try {
                horaIngreso = LocalDateTime.parse(horaTexto, FORMATTER);
            } catch (DateTimeParseException e) {
                mostrarAlerta(Alert.AlertType.WARNING, "Formato Inválido", "La hora de ingreso debe tener el formato: yyyy-MM-dd HH:mm:ss");
                return;
            }
        }

        // Actualizar en el objeto perteneciente al ArrayList
        seleccionado.setTipoVehiculo(tipo);
        seleccionado.setPropietario(propietario);
        seleccionado.setHoraIngreso(horaIngreso);
=======
        // Actualizar en el objeto perteneciente al ArrayList
        seleccionado.setTipoVehiculo(tipo);
        seleccionado.setPropietario(propietario);
        if (!hora.isEmpty()) {
            seleccionado.setHoraIngreso(hora);
        }
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2

        listarVehiculos();
        tblVehiculos.refresh();
        lblEstado.setText("Vehículo " + seleccionado.getPlaca() + " actualizado.");
        mostrarAlerta(Alert.AlertType.INFORMATION, "Actualización Exitosa", "Los datos del vehículo han sido modificados.");
    }

    /**
<<<<<<< HEAD
     * CRUD: Eliminar / Salida y Cobro
     * Procesa la salida del vehículo seleccionado calculando el tiempo total transcurrido
     * y el monto exacto a pagar aplicando la tarifa fija por hora (hora o fracción).
     * Muestra una alerta (Alert) detallada y solicita confirmación antes de removerlo de la lista.
=======
     * CRUD: Eliminar (Registrar Salida)
     * Remueve el vehículo del ArrayList<Vehiculo> tras confirmación.
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2
     */
    @FXML
    public void onEliminar() {
        Vehiculo seleccionado = tblVehiculos.getSelectionModel().getSelectedItem();
        if (seleccionado == null) {
<<<<<<< HEAD
            mostrarAlerta(Alert.AlertType.WARNING, "Selección Requerida", "Seleccione un vehículo de la tabla para procesar su cobro y salida.");
            return;
        }

        LocalDateTime horaSalida = LocalDateTime.now();
        long horasACobrar = seleccionado.calcularHorasACobrar(horaSalida);
        double tarifaPorHora = Vehiculo.TARIFA_POR_HORA;
        double totalAPagar = seleccionado.calcularCobro(horaSalida, tarifaPorHora);
        String tiempoFormateado = seleccionado.obtenerTiempoFormateado(horaSalida);

        String tarifaStr = String.format(Locale.GERMANY, "$%,d COP", (long) tarifaPorHora);
        String totalStr = String.format(Locale.GERMANY, "$%,d COP", (long) totalAPagar);

        Alert alertaCobro = new Alert(Alert.AlertType.CONFIRMATION);
        alertaCobro.setTitle("Liquidación de Parqueadero - Salida y Cobro");
        alertaCobro.setHeaderText("Recibo de Salida - Vehículo [" + seleccionado.getPlaca() + "]");

        String mensaje = "📋 INFORMACIÓN DEL VEHÍCULO:\n"
                + "   • Placa: " + seleccionado.getPlaca() + "\n"
                + "   • Propietario: " + seleccionado.getPropietario() + "\n"
                + "   • Tipo: " + seleccionado.getTipoVehiculo() + "\n"
                + "   • Hora de Ingreso: " + seleccionado.getHoraIngresoFormateada() + "\n"
                + "   • Hora de Salida:  " + horaSalida.format(FORMATTER) + "\n\n"
                + "⏱️ TIEMPO TRANSCURRIDO:\n"
                + "   • Tiempo estacionado: " + tiempoFormateado + "\n"
                + "   • Horas a liquidar (hora o fracción): " + horasACobrar + " hora(s)\n\n"
                + "💰 LIQUIDACIÓN DE PAGO:\n"
                + "   • Tarifa por hora: " + tarifaStr + "\n"
                + "   • TOTAL EXACTO A PAGAR: " + totalStr + "\n\n"
                + "¿Desea confirmar el cobro y registrar la salida del vehículo?";

        alertaCobro.setContentText(mensaje);

        ButtonType btnConfirmar = new ButtonType("Pagar y Registrar Salida", ButtonBar.ButtonData.OK_DONE);
        ButtonType btnCancelar = new ButtonType("Cancelar", ButtonBar.ButtonData.CANCEL_CLOSE);
        alertaCobro.getButtonTypes().setAll(btnConfirmar, btnCancelar);

        Optional<ButtonType> resultado = alertaCobro.showAndWait();
        if (resultado.isPresent() && resultado.get() == btnConfirmar) {
            listaVehiculos.remove(seleccionado);
            listarVehiculos();
            limpiarFormulario();
            lblEstado.setText(String.format("Salida procesada: %s | Pago recibido: %s", seleccionado.getPlaca(), totalStr));
            mostrarAlerta(Alert.AlertType.INFORMATION, "Salida Registrada con Éxito",
                    String.format("El vehículo %s ha cancelado %s y ha salido del parqueadero.", seleccionado.getPlaca(), totalStr));
        } else {
            lblEstado.setText("Operación de salida cancelada para el vehículo " + seleccionado.getPlaca());
=======
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
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2
        }
    }

    /**
<<<<<<< HEAD
     * Alias para compatibilidad con botones o invocaciones de 'Salida / Cobrar'.
     */
    @FXML
    public void onSalidaCobrar() {
        onEliminar();
    }

    /**
=======
>>>>>>> 5f104091666ebabfd107cec0031a1953cc8afdd2
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
