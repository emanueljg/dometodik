let tagSelectMarker = "(*) ";

function tagIsSelected(button) {
  return button.textContent.startsWith(tagSelectMarker);
}

function toggleTagSelected(button) {
  let parts = button.textContent.split(tagSelectMarker);
  if(parts.length > 1) {  // is selected, deselect
    button.textContent = parts[1];
  } else {  // is not selected, select
    button.textContent = tagSelectMarker + parts[0];
  }
}

function showContent(buttonId, contentId) {
  // start by clearing button style
  let btns = document.getElementsByClassName('tag');
  for (var i = 0; i < btns.length; i++) {
    let btn = btns[i];
    if(tagIsSelected(btn)) toggleTagSelected(btn);
    btns[i].style.color = '#fff';
    btns[i].style.backgroundColor = '#000';
  }

  let btn = document.getElementById(buttonId);
  btn.style.color = '#000';
  btn.style.backgroundColor = '#fff';
  toggleTagSelected(btn);
  
  let contents = document.getElementsByClassName('content');
  for (var i = 0; i < contents.length; i++) {
    contents[i].style.display = 'none';
  }
  document.getElementById(contentId).style.display = 'block';
}

window.onbeforeunload = function () {
    window.scrollTo(0,0);
};