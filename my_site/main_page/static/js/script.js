var csrftoken = "{{ csrf_token }}"

document.getElementById("post-like").onclick = () => {
    const requestObject = new XMLHttpRequest()
    requestObject.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            window.location.reload()
        }
    }
    requestObject.open("POST", '/like/')
    requestObject.setRequestHeader("X-CSRFToken", csrftoken)
    const data = new FormData()
    data.append("id", "{{ post.id }}")
    data.append("is_comment", "0")
    requestObject.send(data)
} 