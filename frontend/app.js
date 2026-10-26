// Función única para hablar con la API
async function api(path = '', method = 'GET', body) {
    const response = await fetch(`/api/inventory${path}`, {
        method,
        headers: body ? { 'Content-Type': 'application/json' } : {},
        body: body ? JSON.stringify(body) : undefined,
    });

    const data = await response.json();
    // Flask devuelve { error: "..." } cuando algo sale mal
    if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
    return data;
}

const listar     = ()                   => api();
const crear      = (name, quantity)     => api('', 'POST', { name, quantity });
const actualizar = (id, name, quantity) => api(`/${id}`, 'PUT', { name, quantity });
const eliminar   = (id)                 => api(`/${id}`, 'DELETE');

const inventoryList = document.getElementById('inventory-list');

// Dibuja la lista en pantalla
function pintarLista(items) {
    // Limpiamos primero, si no los productos se duplican en cada recarga
    inventoryList.innerHTML = '';

    items.forEach(item => {
        const listItem = document.createElement('li');

        const itemName = document.createElement('span');
        itemName.className = 'item-name';
        itemName.textContent = item.name;

        const itemQuantity = document.createElement('span');
        itemQuantity.className = 'item-quantity';
        itemQuantity.textContent = `Cantidad: ${item.quantity}`;

        // Botón para eliminar ESTE producto
        const deleteButton = document.createElement('button');
        deleteButton.className = 'btn btn--danger';
        deleteButton.textContent = 'Eliminar';
        deleteButton.addEventListener('click', async () => {
            try {
                await eliminar(item.id);
                await cargar();   // refrescamos la pantalla
            } catch (error) {
                alert(error.message);
            }
        });

        listItem.append(itemName, itemQuantity, deleteButton);
        inventoryList.appendChild(listItem);
    });
}

// Pide la lista al servidor y la dibuja
async function cargar() {
    try {
        pintarLista(await listar());
    } catch (error) {
        console.error('Error al cargar el inventario:', error);
        inventoryList.innerHTML = '<li>Error al cargar los datos.</li>';
    }
}

// Cuando la página termina de cargar, mostramos el inventario
document.addEventListener('DOMContentLoaded', cargar);
