window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        scrollToTop: function(n) {
            const el = document.getElementById('pics');
            if (el) el.scrollTop = 0;
            return null;
        }
    }
});
