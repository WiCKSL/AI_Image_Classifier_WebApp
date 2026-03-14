function previewImage(input) {

    const file = input.files[0]

    const previewBox = document.getElementById("previewBox")
    const preview = document.getElementById("preview")

    if (file) {

        preview.src = URL.createObjectURL(file)

        previewBox.style.display = "block"

    }

}

function showLoader() {

    document.getElementById("loader").style.display = "block"

}