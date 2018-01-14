$(document).foundation();

function trackPlaceClick(placeName) {
    gtag('event', 'view_item', {'items': [placeName]});
}

function trackPlaceForm() {
    gtag('event', 'view_item', {'items': ['placeForm']});
}

$('a.typeform-share').on('click', trackPlaceForm);

$('a[data-place]').on('click', function() {
    var placeName = this.dataset.place;
    if (placeName) {
        trackPlaceClick(placeName);
    }
});

$(document).ready(function() {
    var socialPhotosContainer = $('ul.social-photos');
    if (socialPhotosContainer.length === 1) {
        generateInstagramPhotoFeed();
    }
});

function generateInstagramPhotoFeed() {
    var socialPhotosContainer = $('ul.social-photos');
    var userName = socialPhotosContainer[0].dataset.slug;
    $.ajax({
        url: 'https://www.instagram.com/' + userName + '/?__a=1',
        type: 'GET',
        success: function(data) {
            var images = data.user.media.nodes;
            for (i = 0; i < images.length; i++) {
                var thumbnails = images[i].thumbnail_resources
                var biggestImage = thumbnails.slice(-1)[0];
                socialPhotosContainer.append('<li class="social-photos__photo"><img src="' + biggestImage.src + '"></li>');
            }
        },
        error: function(data){
            console.log(data); // send the error notifications to console
        }
    });
}
