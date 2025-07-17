# Informe de Funcionalidades y Capacidades del Sistema TMS GAVAL

**Versión:** 3.0 (Q3 2024)
**Autor:** Jules, Ingeniero de Software

## 1. Resumen Ejecutivo

El TMS GAVAL es una plataforma de software como servicio (SaaS) diseñada para la gestión integral y optimización de flotas de vehículos. Construido sobre una robusta arquitectura **multi-tenant**, el sistema garantiza que cada empresa cliente opere en un entorno de datos completamente aislado y seguro.

El propósito de esta plataforma va más allá del simple registro de datos; busca ser un **asistente proactivo e inteligente** para los gestores de flotas, proporcionando herramientas para la optimización de costos, la mejora de la disponibilidad de los vehículos, la predicción de fallas y la automatización de procesos clave.

---

## 2. Arquitectura del Sistema

*   **Multi-Tenant Real:** Cada cliente (tenant) opera en su propio esquema dentro de una única base de datos PostgreSQL. Esto asegura un aislamiento total de los datos (vehículos, OTs, usuarios, etc.) entre clientes.
*   **API-First:** La plataforma está diseñada con una API RESTful completa, permitiendo integraciones con sistemas externos como ERPs, sistemas de contabilidad o proveedores de GPS.
*   **Asincronía:** Utiliza Celery y Redis para delegar tareas pesadas (generación de reportes, evaluación de alertas) a un segundo plano, asegurando que la interfaz de usuario sea siempre rápida y responsiva.
*   **Rendimiento Optimizado:** La plataforma incorpora múltiples capas de optimización, incluyendo el cacheo de datos con Redis y la optimización de consultas a la base de datos para garantizar la escalabilidad.

---

## 3. Desglose de Módulos y Funcionalidades

### 3.1. Módulo de Flota y Activos

*   **Gestión de Vehículos:** Creación y seguimiento de cada vehículo de la flota con información detallada (patente, chasis, motor, modelo, norma Euro, etc.).
*   **Historial del Vehículo:** Trazabilidad completa de cada evento en la vida de un vehículo, incluyendo todas las OTs, mantenimientos, y futuras inspecciones.
*   **Actualización de Kilometraje:** Permite la actualización manual o **automática** a través de la integración con GPS.

### 3.2. Módulo de Mantenimiento

*   **Órdenes de Trabajo (OTs):** Sistema completo para gestionar OTs de tipo **Preventiva, Correctiva y Evaluativa**.
*   **Flujo de Estados:** Las OTs pasan por un flujo de estados claro (Pendiente, En Proceso, Pausada, Finalizada), registrando cada cambio en un historial.
*   **Pautas de Mantenimiento:** Creación de pautas de mantenimiento estandarizadas por modelo de vehículo, asociadas a un kilometraje específico.
*   **Pizarra de Programación:** Un calendario interactivo de "arrastrar y soltar" para planificar y asignar OTs a los mecánicos, con indicadores visuales de estado y disponibilidad de repuestos.

### 3.3. Módulo de Inventario

*   **Gestión de Repuestos:** Inventario detallado de repuestos con número de parte, stock actual, stock mínimo, ubicación y proveedor.
*   **Control de Stock:** Registro de todos los movimientos de stock (entradas, salidas por OT, ajustes), manteniendo el inventario siempre actualizado.

### 3.4. Módulo de Neumáticos

*   **Ciclo de Vida del Neumático:** Gestión individual de cada neumático desde su compra hasta su desecho.
*   **Hoja de Vida:** Historial completo de montajes, rotaciones, kilometraje acumulado e inspecciones para cada neumático.
*   **Alertas de Desgaste:** El sistema notifica automáticamente cuando un neumático alcanza su límite de desgaste o un umbral de kilometraje predefinido.

### 3.5. Módulo de Control de Combustible

*   **Registro de Cargas:** Formulario para registrar cada carga de combustible, incluyendo litros, costos y kilometraje.
*   **Cálculo de Rendimiento:** El sistema calcula automáticamente el rendimiento (Km/L) entre cargas, proporcionando una métrica clave para la eficiencia del vehículo.
*   **Análisis de Rendimiento:** Paneles para analizar y comparar el rendimiento por vehículo, ruta o conductor.

### 3.6. Módulo de Business Intelligence y KPIs

*   **Dashboards Personalizables:** Los usuarios pueden crear sus propios dashboards, arrastrando y soltando los widgets de KPIs que más les interesen.
*   **KPIs de Flota:** Disponibilidad, Confiabilidad, Utilización.
*   **KPIs de Mantenimiento:** Análisis de OTs Preventivas vs. Correctivas.
*   **Análisis de Fallas (Pareto):** Un diagrama de Pareto que identifica automáticamente las pocas fallas vitales que causan la mayoría del tiempo de inactividad.
*   **KPIs de RR.HH.:** Medición de la Productividad, Cumplimiento de Planificación y Utilización del equipo técnico.
*   **Reportes Exportables:** Generación de reportes en formato CSV para análisis externo.

### 3.7. Módulo de Alertas y Automatización

*   **Motor de Alertas Personalizables:** Los administradores pueden crear sus propias reglas de negocio para recibir alertas (ej. "Notificar si el Costo/KM de un vehículo supera X valor durante Y días").
*   **Tareas Asíncronas:** La generación de reportes y la evaluación de alertas se realizan en segundo plano para no afectar la experiencia del usuario.
*   **Sistema de Notificaciones:** Un centro de notificaciones en la app informa a los usuarios sobre eventos relevantes (alertas, reportes listos, tareas solicitadas, etc.).

### 3.8. Plataforma y Extensibilidad

*   **API RESTful:** Permite la integración segura con sistemas de terceros.
*   **Integración con GPS:** Un endpoint (webhook) dedicado permite recibir datos de proveedores de telemática para automatizar la actualización de datos críticos.
*   **Progressive Web App (PWA):** La aplicación es instalable en dispositivos móviles, ofreciendo una experiencia similar a una app nativa y capacidades offline.

---

## 4. Roles de Usuario

*   **Administrador/Gerente:** Acceso completo a todos los módulos, incluyendo la configuración, gestión de usuarios, KPIs y creación de reglas de alerta.
*   **Supervisor:** Acceso a la mayoría de los módulos operativos. Puede asignar OTs, gestionar inventario y supervisar al equipo. No puede gestionar usuarios ni configuración crítica.
*   **Mecánico:** Acceso restringido a las OTs que tiene asignadas. Puede ver los detalles de sus tareas, cambiar estados y solicitar nuevas tareas.
*   **Conductor (a través de la PWA):** Puede realizar los checklists de inspección pre-viaje y reportar fallas.

---

## 5. (Próximamente) Panel de Super Administrador

*   Una vista global, accesible solo por el dueño del sistema, que permitirá agregar y comparar KPIs entre todos los tenants, ofreciendo una herramienta de consultoría y análisis de alto nivel.
