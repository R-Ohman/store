function addListenersToInputs() {
    const fileInput = document.querySelector('.custom-file-input');
    const label = document.querySelector('.custom-file-label');

    fileInput.addEventListener('change', (event) => {
        const fileName = event.target.files[0].name;
        label.textContent = fileName;
});


const quantityInputs = document.querySelectorAll('.basket-quantity');
quantityInputs.forEach((input) => {
    input.addEventListener('change', (event) => {
        const quantity = event.target.value;
        const basketId = parseInt(event.target.dataset.basketId, 10);
        const inputElement = event.target; // Сохраняем ссылку на входной элемент
        const csrfToken = document.querySelector('[data-csrf-token]').dataset.csrfToken; // Получаем CSRF-токен


        // Отправить AJAX-запрос на сервер для обновления количества объектов в базе
        // Например, можно использовать Fetch API или библиотеку Axios

        // Пример с использованием Fetch API:
        fetch(`/products/basket/update/${basketId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Используем полученный CSRF-токен
            },
            body: JSON.stringify({ quantity: quantity })
        })
        .then(response => response.json())
        .then(data => {
            // Обновить информацию на странице
            const totalQuantityElement = document.querySelector('.total_quantity');
            const totalSumElement = document.querySelector('.total_sum');
            const productSumWithoutDiscountElement = document.querySelector('#product-' + basketId);
            const productSumElement = document.querySelector('#product-discount-' + basketId);

            if (totalQuantityElement && totalSumElement && productSumElement) {
                totalQuantityElement.textContent = data.total_quantity.toLocaleString('en-EN');
                totalSumElement.textContent = data.total_sum.toLocaleString('en-EN', { minimumFractionDigits: 2 });
                if (productSumElement) {
                    productSumElement.textContent = data.product_sum.toLocaleString('en-EN', {minimumFractionDigits: 2});
                }
                productSumWithoutDiscountElement.textContent = data.product_sum_without_discount.toLocaleString('en-EN', {minimumFractionDigits: 2});
                event.target.value = data.quantity;
            }
        })
        .catch(error => {
            console.error('Error when updating the quantity in the cart: ', error);
            inputElement.value = inputElement.defaultValue; // Используем сохраненную ссылку для изменения значения
        });
    });
});
}

// Вызываем функцию добавления листенеров при загрузке страницы
document.addEventListener('DOMContentLoaded', addListenersToInputs);


$(document).on('click', '.delete-basket', function(e) {
      e.preventDefault();
      var basketId = $(this).data('basket-id');
      deleteBasket(basketId);
    });


function deleteBasket(basketId) {
  var csrfToken = document.querySelector('[data-csrf-token]').dataset.csrfToken;
  fetch('/products/basket/delete/' + basketId + '/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        $('#basket-list').html(data.basket_list_html);
        addListenersToInputs(); // Пересоздаем листенеры после обновления HTML-шаблона
      } else {
        console.error('Error when deleting an item from the cart');
      }
    })
    .catch(error => {
      console.error('Error when deleting an item from the cart:', error);
    });
}