document.addEventListener("DOMContentLoaded", function () {
    const catalogoContainer = document.getElementById("catalogo");

    fetch('/obtener_productos')
        .then(response => response.json())
        .then(productos => {
            productos.forEach((producto) => {
                const card = document.createElement("div");
                card.classList.add("col-sm-6", "col-md-4", "col-lg-3", "mb-4");
                card.innerHTML = `
                    <div class="card">
                        <img src="${producto[2]}" class="img-fluid mx-auto d-block" id="imagenCatalogo" alt="Producto ${producto.id}">
                        <div class="card-body">
                            <h3 class="card-title">${producto[1]}</h3>
                            <p class="card-text">$${producto[3]}</p>
                            <input type="text" class="card-input" id="cantidadProducto${producto.id}" placeholder="Ingresa la cantidad"/>
                            <button class="btn btn-custom btn-agregar">Agregar</button>
                        </div>
                    </div>
                `;
                catalogoContainer.appendChild(card);
            });
        })
        .catch(error => {
            console.error('Error al obtener los productos:', error);
        });

    // Delegación de eventos para el botón "Agregar"
    catalogoContainer.addEventListener("click", function (event) {
        if (event.target.classList.contains("btn-agregar")) {
            const cardBody = event.target.closest(".card-body");
            const cantidad = parseInt(cardBody.querySelector("input").value);
            const producto = getProductDataFromCard(cardBody);

            if (cantidad > 0) {
                agregarProductoAlCarrito(producto, cantidad);
            }
        }
    });

    // Función para obtener los datos del producto desde la tarjeta
    function getProductDataFromCard(cardBody) {
        const titulo = cardBody.querySelector(".card-title").textContent;
        const precio = parseFloat(cardBody.querySelector(".card-text").textContent.replace("$", ""));
        // Aquí podrías también obtener la imagen u otros datos necesarios

        return { nombre: titulo, precio }; // Retorna un objeto con los datos del producto
    }

    // Función para agregar producto al carrito
    const carrito = [];

    function agregarProductoAlCarrito(producto, cantidad) {
        const productoEnCarrito = carrito.find(item => item.producto.nombre === producto.nombre);

        if (productoEnCarrito) {
            productoEnCarrito.cantidad += cantidad;
        } else {
            carrito.push({ producto, cantidad });
        }

        actualizarResumenCompra();
    }

    // Función para actualizar el resumen de la compra
    function actualizarResumenCompra() {
        const resumenCompra = document.getElementById("resumenCompra");
        resumenCompra.innerHTML = "";
        let subtotalTotal = 0;

        carrito.forEach((item) => {
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td>${item.producto.nombre}</td>
                <td class="cantidad-producto-tabla">${item.cantidad}</td>
                <td>$${item.producto.precio * item.cantidad}</td>
            `;
            resumenCompra.appendChild(fila);

            subtotalTotal += item.producto.precio * item.cantidad;
        });

        const total = document.getElementById("total");
        total.textContent = `$${subtotalTotal}`;

        localStorage.setItem('carrito', JSON.stringify(carrito));
    }

    // Botón para finalizar compra
    const botonFinalizarCompra = document.getElementById("botonFinalizarCompra");
    botonFinalizarCompra.addEventListener("click", function (event) {
        localStorage.setItem('total', total.textContent);
        window.location.href = "ticket"; // Redirigir a la página de ticket
    });

    // Otras funciones y código relacionado con la tienda...
});
