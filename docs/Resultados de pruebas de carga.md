## Resultados de pruebas de carga (`POST /predict`)

Pruebas ejecutadas con `scripts/carga.py` contra `https://proyecto-equipo3.onrender.com` utilizando **20 peticiones simultáneas** y un arreglo válido de **30 medidas** en el campo `medidas`.

| Escenario de prueba | Éxitos | Peticiones / s | p50 | p95 |
| :--- | :--- | :--- | :--- | :--- |
| **50 peticiones** | 50 / 50 (100 %) | 32.4 | 479 ms | 823 ms |
| **200 peticiones** | 200 / 200 (100 %) | 48.7 | 360 ms | 553 ms |
| **500 peticiones** | 500 / 500 (100 %) | 46.4 | 424 ms | 557 ms |
| **Tras 20 min sin uso (arranque en frío)** | 50 / 50 (100 %) | 2.2 | 357 ms | 22582 ms |

### Observaciones principales

* **Confiabilidad sin errores:** En las cuatro pruebas se obtuvo el 100 % de respuestas exitosas (`200 OK`) una vez que se ajustó el payload a las 30 variables requeridas por el modelo.
* **Rendimiento en servicio activo:** Con el contenedor ya iniciado, el rendimiento se mantuvo entre **32.4 y 48.7 peticiones/s**, con medianas (`p50`) de **360 a 479 ms** y percentiles 95 (`p95`) entre **553 y 823 ms** incluso al escalar hasta 500 peticiones.
* **Impacto del arranque en frío:** Tras 20 minutos de inactividad, el `p95` subió hasta **22582 ms** (~22.6 s) y el rendimiento cayó a **2.2 peticiones/s** mientras el servicio despertaba, pero la mediana (`p50 = 357 ms`) mostró que el resto de las peticiones respondieron con normalidad una vez activo.