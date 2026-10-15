package app.parqueadero.model;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Objects;

/**
 * Modelo que representa un vehículo dentro del sistema de parqueadero.
 */
public class Vehiculo {

    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private String placa;
    private String tipoVehiculo;
    private String propietario;
    private String horaIngreso;

    public Vehiculo() {
        this("", "", "", LocalDateTime.now().format(FORMATTER));
    }

    public Vehiculo(String placa, String tipoVehiculo, String propietario) {
        this(placa, tipoVehiculo, propietario, LocalDateTime.now().format(FORMATTER));
    }

    public Vehiculo(String placa, String tipoVehiculo, String propietario, String horaIngreso) {
        this.placa = (placa != null) ? placa.trim().toUpperCase() : "";
        this.tipoVehiculo = tipoVehiculo;
        this.propietario = propietario;
        this.horaIngreso = horaIngreso;
    }

    // Getters y Setters
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

    public String getHoraIngreso() {
        return horaIngreso;
    }

    public void setHoraIngreso(String horaIngreso) {
        this.horaIngreso = horaIngreso;
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
                ", horaIngreso='" + horaIngreso + '\'' +
                '}';
    }
}
