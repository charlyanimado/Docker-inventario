// Espera a que el contenido de la página esté cargado
document.addEventListener('DOMContentLoaded', () => {
    
    const inventoryList = document.getElementById('inventory-list');
    
    // Hacemos la petición a nuestra API de Python.
    // Nginx redirige /api/ al backend, así que sirve igual en local y en EC2
    fetch('/api/inventory')
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            // Limpiamos la lista por si había algo antes
            inventoryList.innerHTML = '';
            
            // Por cada item en los datos, creamos un elemento <li> y lo añadimos
            data.forEach(item => {
                const listItem = document.createElement('li');
                
                const itemName = document.createElement('span');
                itemName.className = 'item-name';
                itemName.textContent = item.name;

                const itemQuantity = document.createElement('span');
                itemQuantity.className = 'item-quantity';
                itemQuantity.textContent = `Cantidad: ${item.quantity}`;
                
                listItem.appendChild(itemName);
                listItem.appendChild(itemQuantity);
                
                inventoryList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error al cargar el inventario:', error);
            inventoryList.innerHTML = '<li>Error al cargar los datos.</li>';
        });
});