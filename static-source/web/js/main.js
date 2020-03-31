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
    var player = new Plyr('#player');
    var audio = document.querySelector('#player');
    if (audio) {
        var episodeName = audio.getAttribute('data-episode');
        var podcastName = audio.getAttribute('data-podcast');
    }

    if (audio && player != false) {
        player.on('playing', function() {
            gtag('event', 'play', {
                'podcast': podcastName,
                'episode': episodeName
            });
        });

        player.on('pause', function() {
            gtag('event', 'pause', {
                'podcast': podcastName,
                'episode': episodeName
            });
        });
    }
});
