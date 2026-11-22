# Reporte Hito 3 — Pruebas de carga y perímetro mínimo

## Pruebas de carga (`POST /predict`)

Pruebas ejecutadas con `scripts/carga.py` contra `https://proyecto-equipo3.onrender.com` con **20 peticiones simultáneas** y un arreglo válido de **30 medidas** en `medidas`[cite: 3, 4].

| Escenario de prueba | Éxitos | Peticiones / s | p50 | p95 |
| :--- | :--- | :--- | :--- | :--- |
| **50 peticiones**[cite: 3] | 50 / 50 (100 %)[cite: 3] | 32.4[cite: 3] | 479 ms[cite: 3] | 823 ms[cite: 3] |
| **200 peticiones**[cite: 3] | 200 / 200 (100 %)[cite: 3] | 48.7[cite: 3] | 360 ms[cite: 3] | 553 ms[cite: 3] |
| **500 peticiones**[cite: 3] | 500 / 500 (100 %)[cite: 3] | 46.4[cite: 3] | 424 ms[cite: 3] | 557 ms[cite: 3] |
| **Tras 20 min sin uso (arranque en frío)**[cite: 4] | 50 / 50 (100 %)[cite: 4] | 2.2[cite: 4] | 357 ms[cite: 4] | 22582 ms[cite: 4] |

### Observaciones de rendimiento
* Una vez ajustado el payload a las 30 medidas del esquema `Tumor`, todas las pruebas alcanzaron 100 % de respuestas exitosas[cite: 1, 3, 4].
* Con el servicio activo, el rendimiento se mantuvo entre **32.4 y 48.7 peticiones/s** y `p50` entre **360 y 479 ms**[cite: 3].
* Tras 20 minutos sin uso, el `p95` subió a **22582 ms** mientras despertaba el servicio, con `p50` de **357 ms** y **2.2 peticiones/s**[cite: 4].

---

## Paso 3. Perímetro mínimo

En Render el servicio queda expuesto únicamente por los puertos **80** y **443** (Render termina HTTPS). Con `curl -I` se comprueba que `http://` redirige a `https://`, que no responde en otros puertos (como el `8000`, donde hubo *timeout*) y que `/docs` sigue visible en esta etapa (se ocultará en el Hito 4)[cite: 5, 6].

| Puerto | Origen | Motivo |
| :--- | :--- | :--- |
| **80 (TCP)** | Internet (`0.0.0.0/0`)[cite: 5] | Recibir peticiones HTTP y redirigirlas a HTTPS[cite: 5]. |
| **443 (TCP)** | Internet (`0.0.0.0/0`)[cite: 5] | Recibir tráfico HTTPS cifrado (terminación TLS en Render) hacia la API y `/docs`[cite: 5]. |
| **Otros puertos (ej. 8000, SSH)** | No expuesto / Denegado[cite: 5] | Mantener el perímetro mínimo y evitar exponer puertos internos o administrativos[cite: 5]. |

### Grupos de seguridad en otro proveedor
En un proveedor con grupos de seguridad (*Security Groups*), se aplicaría denegación por defecto y se permitirían entradas únicamente en los puertos **80** y **443** desde el origen autorizado (por ejemplo `0.0.0.0/0` o el balanceador/proxy), restringiendo accesos administrativos (como SSH en el puerto `22`) solo a la IP del equipo y cerrando el resto de puertos[cite: 5].