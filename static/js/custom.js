$(function () {
    $(".word-cloud").jQCloud(word_list, {
        delayedMode: word_list.length > 50,
        shape: false, // or 'rectangular'
        encodeURI: true,
        removeOverflowing: true
    });

  $('[data-toggle="tooltip"]').tooltip()
});

