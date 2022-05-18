// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table

    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all its keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    for (let i=0; i<filterValue.length; i++) {
        items.pop()
    }

    return items
}

function toggleTheme() {
    let body = document.body;
    body.classList.toggle("dark-mode");
    console.log("toggle theme");
}

function toggleTxt() {
  var txt = document.getElementById("theme-button");
  if (txt.innerHTML === "Change Theme to Dark") {
    txt.innerHTML = "Change Theme to Light";
  } else {
    txt.innerHTML = "Change Theme to Dark";
  }
}

function increaseFont(id, increaseFactor) {
    let txt = document.getElementById(id);
    let style = window.getComputedStyle(txt, null).getPropertyValue('font-size');
    let currentSize = parseFloat(style);
    txt.style.fontSize = (currentSize + increaseFactor) + 'px';
    console.log("increaseFont");
}

function decreaseFont(id, decreaseFactor) {
    let txt = document.getElementById(id);
    let style = window.getComputedStyle(txt, null).getPropertyValue('font-size');
    let currentSize = parseFloat(style);
    txt.style.fontSize = (currentSize + decreaseFactor) + 'px';
    console.log("decreaseFont")
}