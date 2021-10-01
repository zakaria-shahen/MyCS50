
// API: Add/Edit/Delete Data
async function add_edit_delete(link, link_view, main_id, id=null, table=null){
    
    let data = {id: id, table: table}  
    // if delete or edit
    const form = document.querySelector(`#${main_id} form`)
    if (form !== null){
        const f = new FormData(form)
        
        for (let p of f.entries()){

            //  if Multiple choice (select multiple )
            if (data[p[0]] !== undefined) {
                
                if (Array.isArray(data[p[0]])) {
                    data[p[0]].push(p[1])
                    continue
                } 

                data[p[0]] = [data[p[0]][0], p[1]]

            }

            // if single choice 
            else {
                data[p[0]] = p[1]
            }
        }
        console.log(data)
    }

    await fetch(link, {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        body: JSON.stringify(data)
    }).then(message => message.text())
    .then((message) => {
        // refresh view
        refresh_view(link_view)
        
        // hidden modal
        modal_hidden_show(main_id, 1)
        
        alert(message)
    })
}

// API: refresh view any table show
async function refresh_view(link_view){
    const view = document.querySelector("#view")
    await fetch(link_view, {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        body: ""
    }).then( (res) => res.text())
    .then((res) => {
        view.innerHTML = res
    }) 
}

// modfiy and show DOM modal delete/edit
function show_delete_edit(status, id, link, link_view, table, name=null){
    // status: 1-> Delete | 2-> Edit 
    // id: this is id data in DB(SQLite3)
    // link: link action (delete or Edit) query API 
    // link_view: link refresh_view on page - API 
    // name: name (user or courses or other)

    let body = ""
    let onclick = ""
    let main_id = ""
    
    // Delete
    if (status === 1){
        main_id = "delete"
        const div_form = document.querySelector(`#${main_id} .modal-content`);

        body = `Do you want to delete ${name} - ID: ${id} ?`
        // insert body
        div_form.querySelector(".modal-body").textContent = body
        onclick = `add_edit_delete("${link}", "${link_view}", "${main_id}",  ${id}, '${table}')`
        div_form.querySelector(".confirm").setAttribute("onclick", onclick)

    }

    // Edit    
    else if (status === 2){
        main_id = 'edit'
        const div_form = document.querySelector(`#${main_id} .modal-content`)

        // Get data from API and Load data on DOM form tag
        search(`id=${id}&table=${table}`).then((data) => {

            // Get DOM form tag and Copy to 'fragment'
            const form = div_form.querySelector("form")
            const fragment = document.createRange().createContextualFragment(form.innerHTML)
            
            // Load data to 'fragment'
            const inputs = fragment.querySelectorAll("input")
            const selects = fragment.querySelectorAll("select")
            for (input of inputs){
                input.value = data[input.name] 
            }

            for (let i = 0; i != selects.length; i++){
                const options = selects[i].querySelectorAll('option')   
                // Remove selected
                options[selects[i].selectedIndex].removeAttribute('selected')

                // Add selected
                options[data[selects[i].name]].setAttribute('selected', '')
            }
            
            // Load 'fragment' to DOM form tag 
            form.replaceChildren(fragment)

            // Add attr 'onclick' in button confirm Edit 
            onclick = `add_edit_delete("${link}", "${link_view}", "${main_id}", ${id})`
            div_form.querySelector(".confirm").setAttribute("onclick", onclick)
        })   
    } 
    
    
    else {
        alert("Error: show_delete_edit(): status value")
        return 
    }

    // show 
    modal_hidden_show(main_id, 2)
}

// show/hiddem modal view 
function modal_hidden_show(main_id, type){
    const div = document.querySelector(`#${main_id}`)

    if (type === 1){
        // hidden
        const modal = bootstrap.Modal.getInstance(div)
        modal.hide()
        modal.toggle()

    } else if (type === 2){
        // show
        const modal = new bootstrap.Modal(div, {
            keyboard: true,
            focus: true
        })

        modal.toggle()
        modal.show() 
    }

}

// alter 
function alert(message, type="primary"){
    const div = document.querySelector("#alert_div")

    const fragment = document.createElement("div")
    fragment.innerHTML = '<div class="alert alert-' + type + ' alert-dismissible" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'

    div.append(fragment)
}

//search by: 1=> ID, other -> soon
// link_qeruy => "id=value&table=value&"
async function search(link_qeruy, by=1){

    if (by === 1){
        // search by ID
        data = ""
        await fetch(`search?${link_qeruy}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json;charset=utf-8"
            }
        }).then((res) => res.json())
        .then((res) => data = res)

        return data
        // const div = document.querySelector("#edit")
    }
   
    

    
}

