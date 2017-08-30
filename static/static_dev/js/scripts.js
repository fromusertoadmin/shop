$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);


    function basketUpdating(product_id, nmb, is_delete){
        var data = {};
        data.product_id = product_id;
        data.nmb = nmb;
         var csrf_token = $('#form_buying_production [name="csrfmiddlewaretoken"]').val();
         data["csrfmiddlewaretoken"] = csrf_token;

        if (is_delete){
            data["is_delete"] = true;
        }

        var url = /basket_adding/; //очень важно сюда запрос с аджакса

        console.log(data)
         $.ajax({
             url: url,
             type: 'POST',
             data: data,
             cache: true,
             success: function (data) {
                 console.log("OK");
                 console.log(data.products_total_nmb);
                 if (data.products_total_nmb || data.products_total_nmb == 0){
                    $('#basket_total_nmb').text("- позиций товаров("+data.products_total_nmb+")");
                     console.log(data.products);
                     $('.basket-items ul').html("");
                     $.each(data.products, function(k, v){
                        $('.basket-items ul').append('<li>'+ v.name+', ' + v.nmb + 'шт. ' + 'по ' + v.price_per_item + 'грн  ' +
                            '<a class="delete-item" href="" data-product_id="'+v.id+'">X</a>'+'<br>'+
                            '</li>');
                      // $('.basket-items ul').append('<li>'+
                      // '<a href="{% url \'checkout\'  %}" class="teste">'
                      //       + 'Оформить заказ' + '</a>' + '</li>');
                      location.reload(true);
                     });
                 }

             },
             error: function(){
                 console.log("error")
             }
         })

    }

    form.on('submit', function(e){
        e.preventDefault();
        console.log('333');
        var nmb = $('#number').val();
        console.log(nmb);
        var submit_btn = $('#submit_btn');
        var product_id =  submit_btn.data("product_id");
        var name = submit_btn.data("name");
        var price = submit_btn.data("price");
        console.log(product_id );
        console.log(name);

        basketUpdating(product_id, nmb, is_delete=false)

    });

    function showingBasket(){
        $('.basket-items').removeClass('hidden');
    };

    function hideBasket(){
        $('.basket-items').addClass('hidden');
    };

    $('.basket-container').on('click', function(e){
        e.preventDefault();
        showingBasket();
    });

     $('.basket-container').mouseover(function(){
         showingBasket();
     });

     $('.basket-container').mouseout(function(){
        hideBasket();
     });

     $('.teste').on('click', function (){
         location.href = " /checkout "
     });

     $('.tester').on('click', function (){
         location.href = " /checkout "
     });

     $(document).on('click', '.delete-item', function(e){
         e.preventDefault();
         product_id = $(this).data("product_id");
         nmb = 0;
         basketUpdating(product_id, nmb, is_delete=true);
     });

     $(".btn-add-to-basket").on('click', function () {
        var supra = $(this);
        var product_id = supra.data("product_id");
        var nmb = 1;
        // console.log("Цена товара" +  my);
        // alert("Айди товара" +  my);
        basketUpdating(product_id, nmb, is_delete=false)
    });

    function calculatingBasketAmount(){
        var total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function() {
            total_order_amount = total_order_amount + parseFloat($(this).text());
        });
        console.log(total_order_amount);
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    }

    $(document).on('change', ".product-in-basket-nmb", function(){
        var current_nmb = $(this).val();
        console.log(current_nmb);

        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        console.log(current_price);
        var total_amount = parseFloat(current_nmb*current_price).toFixed(2);
        console.log(total_amount);
        current_tr.find('.total-product-in-basket-amount').text(total_amount);

        calculatingBasketAmount();
    });


    calculatingBasketAmount();


});