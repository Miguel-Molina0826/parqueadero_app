package app.parqueadero.model;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Objects;

/**
 * Modelo que representa un vehículo dentro del sistema de parqueadero.
 * Gestiona la fecha y hora de ingreso mediante LocalDateTime y provee
 * la lógica de negocio para liquidar el cobro por horas de estacionamiento.
 */
public class Vehiculo {

    public static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    public static final double TARIFA_POR_HORA = 2000.0;

    private String placa;
    private String tipoVehiculo;
    private String propietario;
    private LocalDateTime horaIngreso;

    public Vehiculo() {
        this("", "", "", LocalDateTime.now());
    }

    public Vehiculo(String placa, String tipoVehiculo, String propietario) {
        this(placa, tipoVehiculo, propietario, LocalDateTime.now());
    }

    public Vehiculo(String placa, String tipoVehiculo, String propietario, LocalDateTime horaIngreso) {
        this.placa = (placa != null) ? placa.trim().toUpperCase() : "";
        this.tipoVehiculo = tipoVehiculo;
        this.propietario = propietario;
        this.horaIngreso = (horaIngreso != null) ? horaIngreso : LocalDateTime.now();
    }

    public Vehiculo(String placa, String tipoVehiculo, String propietario, String horaIngresoStr) {
        this(placa, tipoVehiculo, propietario, parseFecha(horaIngresoStr));
    }

    /**
     * Parsea una cadena de texto a LocalDateTime utilizando el formato 'yyyy-MM-dd HH:mm:ss'.
     * Si la cadena es nula o inválida, retorna la fecha y hora actual.
     */
    public static LocalDateTime parseFecha(String fechaStr) {
        if (fechaStr == null || fechaStr.isBlank()) {
            return LocalDateTime.now();
        }
        try {
            return LocalDateTime.parse(fechaStr.trim(), FORMATTER);
        } catch (DateTimeParseException e) {
            return LocalDateTime.now();
        }
    }

    // ==========================================
    // MÉTODOS DE LÓGICA DE NEGOCIO (COBRO Y TIEMPO)
    // ==========================================

    /**
     * Calcula los minutos transcurridos desde el ingreso hasta la hora de salida especificada.
     *
     * @param horaSalida Fecha y hora al momento de registrar la salida.
     * @return Minutos transcurridos (mínimo 0).
     */
    public long calcularMinutosEstacionado(LocalDateTime horaSalida) {
        if (this.horaIngreso == null || horaSalida == null) {
            return 0;
        }
        long minutos = Duration.between(this.horaIngreso, horaSalida).toMinutes();
        return Math.max(0, minutos);
    }

    public long calcularMinutosEstacionado() {
        return calcularMinutosEstacionado(LocalDateTime.now());
    }

    /**
     * Calcula el número de horas a facturar según la regla estándar de parqueadero
     * (cobro por hora o fracción de hora).
     * Por ejemplo:
     * - De 1 a 60 minutos: 1 hora
     * - De 61 a 120 minutos: 2 horas
     * - Si transcurrieron 0 minutos (salida en el mismo minuto): mínimo 1 hora de servicio.
     *
     * @param horaSalida Momento de salida del vehículo.
     * @return Horas a cobrar (mínimo 1).
     */
    public long calcularHorasACobrar(LocalDateTime horaSalida) {
        long minutos = calcularMinutosEstacionado(horaSalida);
        if (minutos <= 0) {
            return 1;
        }
        return (long) Math.ceil((double) minutos / 60.0);
    }

    public long calcularHorasACobrar() {
        return calcularHorasACobrar(LocalDateTime.now());
    }

    /**
     * Calcula el valor total exacto a pagar aplicando la tarifa fija por hora (hora o fracción).
     *
     * @param horaSalida    Momento de salida del vehículo.
     * @param tarifaPorHora Tarifa fija por hora (ej. 2000).
     * @return Monto exacto a pagar.
     */
    public double calcularCobro(LocalDateTime horaSalida, double tarifaPorHora) {
        long horasACobrar = calcularHorasACobrar(horaSalida);
        return horasACobrar * tarifaPorHora;
    }

    public double calcularCobro(LocalDateTime horaSalida) {
        return calcularCobro(horaSalida, TARIFA_POR_HORA);
    }

    public double calcularCobro() {
        return calcularCobro(LocalDateTime.now(), TARIFA_POR_HORA);
    }

    public double calcularValorAPagar(LocalDateTime horaSalida, double tarifaPorHora) {
        return calcularCobro(horaSalida, tarifaPorHora);
    }

    public double calcularValorAPagar() {
        return calcularCobro();
    }

    /**
     * Retorna una representación amigable del tiempo total transcurrido.
     * Ejemplo: "1 hora(s) y 15 minuto(s) (75 minutos en total)"
     *
     * @param horaSalida Momento de salida del vehículo.
     * @return Cadena formateada con horas y minutos.
     */
    public String obtenerTiempoFormateado(LocalDateTime horaSalida) {
        long minutosTotales = calcularMinutosEstacionado(horaSalida);
        long horas = minutosTotales / 60;
        long minutosRestantes = minutosTotales % 60;
        return String.format("%d hora(s) y %d minuto(s) (%d minutos en total)", horas, minutosRestantes, minutosTotales);
    }

    public String obtenerTiempoFormateado() {
        return obtenerTiempoFormateado(LocalDateTime.now());
    }

    // ==========================================
    // GETTERS Y SETTERS
    // ==========================================

    public String getPlaca() {
        return placa;
    }

    public void setPlaca(String placa) {
        this.placa = (placa != null) ? placa.trim().toUpperCase() : "";
    }

    public String getTipoVehiculo() {
        return tipoVehiculo;
    }

    public void setTipoVehiculo(String tipoVehiculo) {
        this.tipoVehiculo = tipoVehiculo;
    }

    public String getPropietario() {
        return propietario;
    }

    public void setPropietario(String propietario) {
        this.propietario = propietario;
    }

    public LocalDateTime getHoraIngreso() {
        return horaIngreso;
    }

    public void setHoraIngreso(LocalDateTime horaIngreso) {
        this.horaIngreso = (horaIngreso != null) ? horaIngreso : LocalDateTime.now();
    }

    public void setHoraIngreso(String horaIngresoStr) {
        this.horaIngreso = parseFecha(horaIngresoStr);
    }

    /**
     * Retorna la hora de ingreso formateada como String para visualización en tablas o formularios.
     */
    public String getHoraIngresoFormateada() {
        return (horaIngreso != null) ? horaIngreso.format(FORMATTER) : "";
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Vehiculo vehiculo = (Vehiculo) o;
        return Objects.equals(placa, vehiculo.placa);
    }

    @Override
    public int hashCode() {
        return Objects.hash(placa);
    }

    @Override
    public String toString() {
        return "Vehiculo{" +
                "placa='" + placa + '\'' +
                ", tipoVehiculo='" + tipoVehiculo + '\'' +
                ", propietario='" + propietario + '\'' +
                ", horaIngreso=" + getHoraIngresoFormateada() +
                '}';
    }
}
