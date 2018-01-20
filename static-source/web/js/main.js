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
    var player = plyr.setup()[0];

    player.on('playing', function(event) {
        var instance = event.detail.plyr;

        var audio = instance.getContainer().querySelector('audio');
        var episodeName = audio.getAttribute('data-episode');
        var podcastName = audio.getAttribute('data-podcast');

        gtag('event', 'play', {
            'podcast': podcastName
            'episode': episodeName
        });
    });

    player.on('pause', function(event) {
        var instance = event.detail.plyr;

        var audio = instance.getContainer().querySelector('audio');
        var podcastName = audio.getAttribute('data-podcast');
        var episodeName = audio.getAttribute('data-episode');

        gtag('event', 'pause', {
            'podcast': podcastName
            'episode': episodeName
        });
    });
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
