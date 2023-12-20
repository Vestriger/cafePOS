$(document).ready(function () {
    var order = JSON.parse(localStorage.getItem('order')) || {};
    console.log(order)
    order['worker_id'] = $('#worker_name').data('worker-id');

    function updateOrder() {
        $.ajax({
            url: '/update_order/',
            type: 'POST',
            data: {'order': JSON.stringify(order)},
            success: function (response) {
                $('.order').html(response.order_html);
                localStorage.setItem('order', JSON.stringify(order));
            }
        });
    }

    updateOrder()

    $('.product_item').on('click', function () {
        var productId = $(this).data('product-id');
        if (productId) {
            if (!(productId in order)) {
                order[productId] = 1;
            } else {
                order[productId] += 1;
            }

            updateOrder();
        }
    });

    $('.order').on('click', '.order_position_cancel', function () {
        var productId = $(this).data('product-id');
        if (productId in order) {
            delete order[productId];
        }
        updateOrder();
    });

    $('.order').on('submit', '#order_button', function (event) {
        event.preventDefault();
        var orderInput = $(this).find('#orderInput');
        orderInput.val(JSON.stringify(order));
        order = {}
        updateOrder()
        this.submit();
    });

     document.getElementById('category_item_new').addEventListener('click', function () {
        document.getElementById('add-category-form-container').style.display = 'flex';
        document.getElementById('add-category-button').style.display = 'none';
    });

     function transliterate(text) {
      const russianToEnglish = {
        а: 'a', б: 'b', в: 'v', г: 'g', д: 'd', е: 'e', ё: 'e', ж: 'zh',
        з: 'z', и: 'i', й: 'y', к: 'k', л: 'l', м: 'm', н: 'n', о: 'o',
        п: 'p', р: 'r', с: 's', т: 't', у: 'u', ф: 'f', х: 'kh', ц: 'ts',
        ч: 'ch', ш: 'sh', щ: 'sch', ь: '', ы: 'y', ъ: '', э: 'e', ю: 'yu',
        я: 'ya'
      };

      return text
        .toLowerCase()
        .replace(/[а-яё]/g, char => russianToEnglish[char] || char)
        .replace(/\s+/g, '-')
        .replace(/[^a-z0-9-]/g, '')
        .replace(/-+/g, '-') //
        .replace(/^-+|-+$/g, '');
    }

    document.getElementById('add-category-form').addEventListener('submit', function (event) {
        event.preventDefault();

        var newCategoryName = document.getElementById('new-category-name').value;

        $.ajax({
            url: '/add_category/',
            type: 'POST',
            data: {'category_name': newCategoryName, 'slug': transliterate(newCategoryName)},
            success: function() {
                window.location.href = '/';
              },
        });
    });

     document.getElementById('add-product-form').addEventListener('submit', function (event) {
        event.preventDefault();

        var newProductName = document.getElementById('new-product-name').value;
        var newProductPrice = document.getElementById('new-product-price').value;
        var categorySlug = $('#add-product-form').data('category-slug');

        console.log({
                'product_name': newProductName,
                'slug': transliterate(newProductName),
                'price': newProductPrice,
                'category_slug': categorySlug
            })

        $.ajax({
            url: '/add_product/',
            type: 'POST',
            data: {
                'product_name': newProductName,
                'slug': transliterate(newProductName),
                'price': newProductPrice,
                'category_slug': categorySlug
            },
            success: function() {
                window.location.href = '/'+categorySlug+'/';
              },
        });
    });


     $(window).on('beforeunload', function () {
    localStorage.setItem('order', JSON.stringify(order));
    });
});