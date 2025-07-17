document.addEventListener('DOMContentLoaded', function () {
    let grid = GridStack.init({
        float: true,
        cellHeight: '70px',
        minRow: 1,
    });

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let dashboardConfig = null;

    const loadDashboard = async () => {
        try {
            const response = await fetch('/api/v1/dashboards/');
            const data = await response.json();
            if (data.results.length > 0) {
                dashboardConfig = data.results[0];
                grid.removeAll();
                dashboardConfig.widgets.forEach(widgetInstance => {
                    loadWidget(widgetInstance);
                });
            } else {
                // Crear un dashboard si no existe
                const newDashboardResponse = await fetch('/api/v1/dashboards/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                    body: JSON.stringify({ nombre: 'Mi Dashboard Principal' })
                });
                dashboardConfig = await newDashboardResponse.json();
            }
        } catch (error) {
            console.error('Error al cargar el dashboard:', error);
        }
    };

    const loadWidget = async (widgetInstance) => {
        try {
            const response = await fetch(`/templates/flota/${widgetInstance.widget.template_name}`);
            const html = await response.text();
            const el = grid.addWidget({
                x: widgetInstance.pos_x,
                y: widgetInstance.pos_y,
                w: widgetInstance.width,
                h: widgetInstance.height,
                content: html,
                id: widgetInstance.id.toString()
            });
        } catch (error) {
            console.error('Error al cargar el widget:', error);
        }
    };

    grid.on('change', async (event, items) => {
        for (const item of items) {
            const widgetId = item.id;
            const newPos = {
                pos_x: item.x,
                pos_y: item.y,
                width: item.w,
                height: item.h,
            };
            try {
                await fetch(`/api/v1/dashboard-widgets/${widgetId}/`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                    body: JSON.stringify(newPos)
                });
            } catch (error) {
                console.error('Error al guardar la posición del widget:', error);
            }
        }
    });

    const editButton = document.getElementById('edit-dashboard-button');
    editButton.addEventListener('click', () => {
        if (grid.opts.static) {
            grid.enable();
            editButton.innerHTML = '<i class="fas fa-save mr-2"></i>Guardar Disposición';
            editButton.classList.remove('!bg-blue-600');
        } else {
            grid.disable();
            editButton.innerHTML = '<i class="fas fa-edit mr-2"></i>Activar Edición';
            editButton.classList.add('!bg-blue-600');
        }
    });

    // Cargar el dashboard al iniciar
    loadDashboard();
});
