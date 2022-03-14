function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function httpGet(theUrl, json=false)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    // console.log(xmlHttp.responseText)
    if (json && xmlHttp.responseText)
        return JSON.parse(xmlHttp.responseText)
    else
        return xmlHttp.responseText;
}

function urlBuilder(cmdApi, k_v) {
    let url = "/api/" + cmdApi
    if (k_v) {
        url += "?"
        for (let [key, value] of k_v) {
            url += key + "=" + value + "&"
        }
    }
    return url
}

function RequestUrl(cmdApi, k_v, json=false) {
    let url = urlBuilder(cmdApi, k_v)
    return httpGet(url, json)
}

const main_list = $("#main-list")
const search_text = $("#search-query")
const current_page = $("#current-page")
window.page = 0
window.max_page = parseInt(RequestUrl("getMaxPage"))
$("#max-page").html("Всего страниц: " + window.max_page)


function load_films() {
    let result = RequestUrl("getFilmsList/" + window.page);
    main_list.html(result)
    current_page.html('<a class="page-link">' + (window.page + 1) +'</a>')
}
load_films()

function next_page() {
    if (window.page + 1 <= window.max_page) {
        window.page++
        load_films()
    }
}

function prev_page() {
    if (window.page - 1 >= 0) {
        window.page--
        load_films()
    }
}

function search() {
    $(".pagination-block").html("")
    $("#max-page").html("")
    let query = search_text.val()
    let result = RequestUrl("searchByTitle/" + query);
    if (!result) {
        result = "<h1 style='color: white'>По запросу '" + query + "' ничего не найдено</h1>"
    }
    main_list.html(result)
    search_text.val("")

}

$("#search-btn").bind("click", search);

$("#search-query").keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
        search()
    }
});

