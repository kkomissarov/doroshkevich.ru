 $(document).ready(function(){

    //Добавление в корзину
    $('body').on('click', '.add-to-cart-btn', function(){
        var data = {
            product_id: $(this).attr('data-product-id'),
            action: 'add'
        };
         $.ajax({
            type: 'GET',
            url: '/json_cart/',
            data: data,
            success: function(data){
                $('span#cart_count').html(data.count)
            }
        })
        $(this).html('<i class="fa fa-check-circle-o" aria-hidden="true"></i> В корзине');
        $(this).addClass('btn-in-cart');
        $(this).removeClass('btn-3');
        $('.add-product-popup').fadeIn(600);
        return false;
    });


    //Наведение на кнопку добавленного товара
    $('body').on('mouseenter', '.btn-in-cart', function(){ 
        $(this).html('<i class="fa fa-plus-circle" aria-hidden="true"></i> Добавить еще')
    })

    $('body').on('mouseleave', '.btn-in-cart', function(){                
        $(this).html('<i class="fa fa-check-circle-o" aria-hidden="true"></i> В корзине')
    });


    //Удаление товаров на страние заказов
    $('.remove_cart_item').on('click', function(){
        var data = {
            product_id: $(this).attr('data-product-id'),
            action: 'delete'
        };
        $(this).closest('tr').remove()
        $.ajax({
            type: 'GET',
            url: '/json_cart/',
            data: data,
            success: function(data){
            	if($('#order-list-table').find('tr').length > 2){
	                $('span#cart_count').html(data.count);
	                $('td#total-price').html(data.total+ ' руб.');
            	}else{
            		$('.cart-form').remove()
            		$('#checkout-settings').remove()
            		$('span#cart_count').html(0);
            		$('.empty-notification').show(200)
            	}

            }
        })
        return false;
    })


    //Изменение количества товара в корзине
    $('.item-qty').change(function(){
        var data = {
            product_id: $(this).attr('data-product-id'),
            action: 'change-qty',
            qty: $(this).val()
        };
        $.ajax({
            type: 'GET',
            url: '/json_cart/',
            data: data,
            success: function(data){
                $('td#total-price').html(data.total+' руб.')
                $('span#cart_count').html(data.count);
            }
        })
        return false;
    })

    $('.cart-form').submit(function(e){
    	e.preventDefault();
    });


	//Добавление товара из карточки
	$('form.cart').submit(function(e){
		e.preventDefault();
		
		var data = {
            product_id: $(this).attr('data-product-id'),
            action: 'add-with-qty',
            qty: $(this).find('input.qty').val()
        };

        $.ajax({
            type: 'GET',
            url: '/json_cart/',
            data: data,
            success: function(data){
                console.log(data);
                $('span#cart_count').html(data.count)
            }
        });
        $('.add-product-popup').fadeIn(600);
        $('.btn-3').html('<i class="fa fa-check-circle-o" aria-hidden="true"></i> В корзине');
        $('.btn-3').addClass('btn-in-cart');
        $('.btn-3').removeClass('btn-3');

	})


	//Закрыть всплывающее окно при добавлении
	$('#continue-shopping').click(function(){
		$('.add-product-popup').fadeOut(600);
		return false;
	});

	$('.add-product-popup').click(function(){
		$('.add-product-popup').fadeOut(600);
		return false;
	});	

	$('.add-product-popup_window').click(function(e){
		e.stopPropagation();
	});	


    //Изменение форм в зависимости от типа доставки
    $('#delivery_type').change(
      function(){
        
        if ($('#delivery_type').val() == 'mkad') {
            $('.cart-form-variant').hide()
            $('#mkad-delivery').fadeIn()
        }

        else if ($('#delivery_type').val() == 'ruspost') {
            $('.cart-form-variant').hide()
            $('#russian-post-delivery').fadeIn()
        }


        else if ($('#delivery_type').val() == 'tk') {
            $('.cart-form-variant').hide()
            $('#tk-delivery').fadeIn()
        }

    });


    $('.lk-nav').find('a').click(
        function(){
            $('.lk-nav').find('a').removeClass('active');
            $(this).addClass('active');
        }
    )

    $('#profile-settings').click(
        function(){
            if ($('#lk-personal-data').is(":hidden")) {
                $('.lk-elem').hide();
                $('#lk-personal-data').fadeIn();
            }    
    });

    
    $('#order-history').click(
        function(){
            if ($('#lk-order-history').is(":hidden")) {
                $('.lk-elem').hide();
                $('#lk-order-history').fadeIn();
            }
    });

//Скрывание и открывание полей при выборе способоа доставки
    $('#delivery_type').change(function(){
        if($(this).val() == 'mkad') {
            $('#cart-tk-wrapper').hide();
            $('#delivery_company').removeAttr('required');
            $('#cart-city-wrapper').hide();
            $('#city').removeAttr('required');

            $('#pay_type').append($('<option>', {
                value: 'cash',
                text: 'Наличными курьеру'})
            )
        }            
        

        else if($(this).val() == 'r_post'){
            $('#cart-tk-wrapper').hide();
            $('#delivery_company').removeAttr('required');
            $('#cart-city-wrapper').show();
            $('#city').attr('required', '')
            
            if($('#pay_type option[value="cash"]')){
                $('#pay_type option[value="cash"]').remove()
            }
        }

        else if($(this).val() == 'tk'){
            $('#cart-city-wrapper').show();
            $('#city').attr('required', '')
            $('#cart-tk-wrapper').show();
            $('#delivery_company').attr('required', '')
            
            if($('#pay_type option[value="cash"]')){
                $('#pay_type option[value="cash"]').remove()
            }
        }
    });

//мобильное меню
    $('.burger').on('click', function(){
      if($('.m-menu').hasClass('m-menu__active')) {
        $('.m-menu').removeClass('m-menu__active')    
      } 
      else{
        $('.m-menu').addClass('m-menu__active') 
        } 
    });


//Маска телефона
    $("#phone").mask("+7 (999) 999-99-99");

});