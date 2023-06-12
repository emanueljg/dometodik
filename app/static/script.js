window.onbeforeunload = function () {
    window.scrollTo(0,0);
};

function showTodoEditor(n) {
  let todo = document.getElementById("todo-" + n)
  // show editor
  todo.getElementById("todo-editor-" + n).style.display = "unset"
  // 
}

function toggleTodoEditor(n) {
  let todo = document.getElementById("todo-" + n)
  let todoDeleter = document.getElementById("todo-deleter-" + n)
  let editor = document.getElementById("todo-editor-" + n)

  if (editor.offsetParent === null) {  // is hidden
    editor.style.display = "inherit";    
    todoDeleter.style.display = "none"

  } else {  // is visible
    editor.reset()
    editor.style.display = "none"
    todoDeleter.style.display = "inherit"
  }
  
}
