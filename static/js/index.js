var obj;
var imgSrc;
var flagContact = 1;

$(function () {
	$('.navbar-item').css('color', 'white');
	$(window).scroll(function() {
	  //为了保证兼容性，这里取两个值，哪个有值取哪一个
	  //scrollTop就是触发滚轮事件时滚轮的高度
//	  var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
//	  // console.log("滚动距离" + scrollTop);
//	  if((scrollTop >= 781 && scrollTop <1551) || scrollTop >= 2387) {
//
//	  	obj = document.getElementById("navbar-logo");
//		obj.src = '../assets/images/logo-dark.svg';
//
//		obj = document.getElementById("avatar-small");
//		obj.src = '../assets/images/login-dark.png';
//
//	  	$('.navbar-item').css('color', 'black');
//	  	$('.navbar').css('background', 'transparent');
//	  	// console.log("滚动距离" + scrollTop);
//	  }
//
//	  if((scrollTop >= 1551 && scrollTop < 2387) || scrollTop < 781) {
//
//	  	obj = document.getElementById("navbar-logo");
//		obj.src = '../assets/images/logo.svg';
//
//		obj = document.getElementById("avatar-small");
//		obj.src = '../assets/images/login.png';
//
//	  	$('.navbar-item').css('color', 'white');
//	  	$('.navbar').css('background', 'rgba(0,0,0,0.5)');
//	  	// console.log("滚动距离" + scrollTop);
//	  }
	})
});

function wechatContact() {
	// console.log(flagContact);
	if(flagContact == 1)
		$('.wechat-contact').css('display', 'block');
	else
		$('.wechat-contact').css('display', 'none');
	
	flagContact = -flagContact;
}

function goToPageOne() {
	$('html, body').animate({  
	  scrollTop: '0px'
	}, 800); 
}

function goToPageTwo() {
	$('html, body').animate({  
	  scrollTop: '814px'   
	}, 800); 
}

function goToPageThree() {
	$('html, body').animate({  
	  scrollTop: '1600px'   
	}, 800); 
}

function goToPageFour() {
	$('html, body').animate({  
	  scrollTop: '2395px'   
	}, 800); 
}

function uploadImage() {
    var formData = new FormData();
    var fileReader = new FileReader();
    var file=document.getElementById('image').files[0];
    fileReader.readAsDataURL(file);

    fileReader.onload = function(e) {
        document.getElementById('image-content').src=this.result;
        formData.append('file', file);
        $.ajax({
            url: "/savefile/",
            type: 'POST',
            data: formData,
            success: function(data) {
                console.log(data);
            },
            error: function(data) {
                console.log(data)
            }
        });
    }
//    reader.readAsDataURL(file);
}