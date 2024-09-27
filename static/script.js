$(document).ready(function() {
    "use strict"; 
    $('#form-inserir-materia').submit(function(event) { 
        event.preventDefault(); 
        $.ajax({ 
            type: 'POST', 
            url: '/inserir_materia', 
            contentType: 'application/json', 
            data: JSON.stringify({ 
                nm_materia: $('#nm_materia').val(), 
                id_usuario: $('#id_usuario').val() 
            }), 
            success: function(response) { 
                f_consultar_materia(); 
                var div_msg_mat = document.getElementById("div_msg_materia"); 
                div_msg_mat.style.display = 'block'; 
                document.getElementById("janela-materia").style.pointerEvents = 'none';
                setTimeout(function() { 
                    div_msg_mat.style.display = 'none'; 
                    fecharJanelaMateria();
                    f_consultar_materia()
                    document.getElementById("janela-materia").style.pointerEvents = 'auto';
                }, 2000); 
                document.getElementById('nm_materia').value = ''; 
                document.getElementById('id_usuario').value = ''; 
            }, 
            error: function(error) { 
                $('#mensagem_pergunta').text('Erro ao inserir a matéria: ' + error.responseJSON.message); 
            } 
        }); 
    }); 
});

$(document).ready(function() {
    "use strict"; 
    $('#form-inserir-pergunta').submit(function(event) { 
        event.preventDefault(); 
        var dados = {};
        $('input[name="radioEscolha"]').each(function() { 
            if ($(this).is(':checked')) { 
                dados['radio'] = $(this).val(); 
            } 
        }); 
        $('textarea').each(function() { 
            var nome = $(this).attr('name'); 
            var valor = $(this).val(); 
            dados[nome] = valor; 
            dados['id'] = $(this).id; 
        }); 
        var selectElement = document.querySelector('#id_topico'); 
        //console.log(dados) 
        $.ajax({ 
            type: 'POST', 
            url: '/inserir_pergunta', 
            contentType: 'application/json', 
            data: JSON.stringify({ 
                id_topico: $('#id_topico').val(), 
                pergunta: $('#pergunta').val(), 
                dados 
            }), 
            success: function(response) { 
                var div_display_alt = document.getElementById("div_msg_incluida"); 
                div_display_alt.style.display = 'block'; 
                setTimeout(function() { 
                    div_display_alt.style.display = 'none'; 
                    const link = document.getElementById('pag-resultados'); 
                    link.href = '/'; 
                    window.location.href = link.href; 
                }, 1000);  
            }, 
            error: function(error) { 
                $('#mensagem_pergunta').text('Erro ao inserir a matéria: ' + error.responseJSON.message); 
            } 
        }); 
    }); 
});

function escolhaResposta(element) { 
    $.ajax({ 
        type: 'POST', 
        url: '/inserir_resposta', 
        contentType: 'application/json', 
        data: JSON.stringify({ 
            id_pergunta: element.id, 
            id_alternativa: element.name, 
            id_usuario: 10145310 
        }), 
        success: function(response) { 
            var msg = response.message.correta 
            if (msg) { 
                element.style.backgroundColor = '#61e98f'; 
            } else { 
                element.style.backgroundColor = '#dc3545'; 
            } 
            var div_display = document.getElementById('div_display_' + element.id); 
            div_display.style.display = 'block'; 
            // Deasabilita clic na Div
            var excluirDiv_perg = document.getElementById('pergunta_' + element.id); 
            excluirDiv_perg.style.pointerEvents="none";             
            setTimeout(function() {                 
                excluirDiv_perg.parentNode.removeChild(excluirDiv_perg); 
                f_consultarDivsPerguntasAtivas()
            }, 1000); 
            
            
        }, 
        error: function(error) { 
            $('#mensagem_index').text('Houve um problema, tente mais tarde.'); 
        } 
    }); 
}

$(document).ready(function() {
    "use strict"; 
    $('#form-inserir-topico-pag').submit(function(event) { 
        event.preventDefault(); 
        var selectElement = document.querySelector('#id_materia'); 
        $.ajax({ 
            type: 'POST', 
            url: '/inserir_topico', 
            contentType: 'application/json', 
            data: JSON.stringify({ 
                id_materia: selectElement.value, 
                nm_topico: $('#nm_topico').val(), 
                id_usuario: 10145310 
            }), 
            success: function(response) { 
                f_consultar_topico(); 
                var div_msg_topi = document.getElementById("div_msg_topico"); 
                div_msg_topi.style.display = 'block'; 
                //console.log(div_msg_topi) 
                setTimeout(function() { 
                    div_msg_topi.style.display = 'none'; 
                    document.getElementById("fechar").onclick(this);                     
                    f_consultar_topico()
                }, 2000); 
            }, 
            error: function(error) { 
                $('#mensagem_topico').text('Erro ao inserir a matéria: ' + error.responseJSON.message); 
            } 
        }); 
    }); 
});
$(document).ready(function() {
    "use strict"; 
    $('#form-inserir-topico').submit(function(event) { 
        event.preventDefault(); 
        var selectElement = document.querySelector('#id_materia'); 
        $.ajax({ 
            type: 'POST', 
            url: '/inserir_topico', 
            contentType: 'application/json', 
            data: JSON.stringify({ 
                id_materia: selectElement.value, 
                nm_topico: $('#nm_topico').val(), 
                id_usuario: 10145310 
            }), 
            success: function(response) { 
                f_consultar_topico(); 
                var div_msg_topi = document.getElementById("div_msg_topico"); 
                div_msg_topi.style.display = 'block'; 
                //console.log(div_msg_topi) 
                document.getElementById("janela").style.pointerEvents = 'none';
                setTimeout(function() { 
                    div_msg_topi.style.display = 'none'; 
                    fecharJanela();
                    f_consultar_materia()
                    document.getElementById("janela").style.pointerEvents = 'auto';
                }, 2000); 
            }, 
            error: function(error) { 
                $('#mensagem_topico').text('Erro ao inserir a matéria: ' + error.responseJSON.message); 
            } 
        }); 
    }); 
});

$(document).ready(function() {
    "use strict"; 
    $('#atualizar_pergunta_forms').submit(function(event) { 
        event.preventDefault(); 
        const formData = new FormData(this); 
        fetch('/atualizar_pergunta_forms', { 
            method: 'POST', 
            body: formData 
        }) 
        .then(response => response.json()) 
        .then(data => { 
            var div_display_alt = document.getElementById("div_msg_alterado"); 
            div_display_alt.style.display = 'block'; 
            setTimeout(function() { 
                div_display_alt.style.display = 'none'; 
                const link = document.getElementById('pag-resultados'); 
                link.href = '/'; 
                window.location.href = link.href; 
            }, 1000); 
        }) 
        .catch(error => { 
            //console.error('Erro ao enviar solicitação:', error); 
        }); 
    }); 
});



document.addEventListener('DOMContentLoaded', function() { 
    var id_divMsg_materia = document.getElementById("mensagem_materia"); 
    if (id_divMsg_materia) { 
        f_consultar_materia()
    } 
    var id_divMsg_topico = document.getElementById("exibir-lista-topicos"); 
    if (id_divMsg_topico) { 
        f_consultar_topico(); 
        f_consultarDivsPerguntasAtivas()
    } 
    var id_div_topicoPerg = document.getElementById("exibir-lista-perguntas"); 
    if (id_div_topicoPerg) { 
        f_consultar_topico_perguntas();
        renderMathInElement(document.getElementById("lista-perguntas-topicos"));
    } 
});


function f_consultar_pergunta() { 
    $.get('/pergunta_con', function(response) { 
        if (response.length > 0) { 
            //console.log(response); 
            var ul = document.getElementById("lista-perguntas"); 
            ul.innerHTML = ''; 
            response.forEach(function(materia){ 
                var li = document.createElement('li'); 
                li.id=materia.id_materia 
                li.className='card-body' 
                var a_item = document.createElement('a'); 
                a_item.href='topicos/'+materia.id_materia 
                a_item.text=materia.id_materia + " - " +materia.nm_materia+materia.dt_criacao_mat; 
                li.appendChild(a_item) 
                ul.appendChild(li); 
            }); 
        } else { 
            $('#mensagem_pergunta').append('Nenhuma pergunta encontrada.'); 
        } 
    }); 
}

function f_consultar_materia() { 
    fetch('/materia_topico_con',{method: 'GET',})    
    .then(response => response.json()) // Converte a resposta para JSON
    .then(response => {
        let materias = Object.values(response);
        var ul = document.getElementById("lista-materia"); 
        ul.innerHTML = ''; 
        materias.forEach(materia => {               //
            var div_col = document.createElement('div'); 
            var div_botao = document.createElement('div'); 
            div_botao.className="card-body hover-div"
            var div_col_button = document.createElement('button'); 
            div_col_button.id="btn-"+materia.id_materia;  
            div_col_button.className="btn btn-outline-info "
            div_col_button.classList.add("materia-interacao");
            div_col_button.textContent="+"
            div_col_button.style.float="right"
            
            div_col_button.addEventListener("click", function() {
                var mostrarDiv = document.getElementById("container_"+materia.id_materia); 
                
                var btn_id = document.getElementById("btn-"+materia.id_materia); 
                //console.log("div-show",mostrarDiv.style.display,btn_id)
                if (mostrarDiv.style.display === "block" ) {
                    mostrarDiv.style.padding= 0;
                    mostrarDiv.style.display = "none";
                    btn_id.textContent="+"
                } else{
                    mostrarDiv.style.display = "block";                    
                    btn_id.textContent="-"
                }
            });
     

            div_col.id=materia.id_materia    ;        
            div_col.className='col  h-auto d-inline-block '  ; 

            var div_conteudo = document.createElement('div'); 
            div_conteudo.id="container_"+(materia.id_materia); 
            div_conteudo.className='card-body' ; // Colocar o 
            var a_item = document.createElement('a'); 
            a_item.text=materia.id_materia + " - " +materia.nm_materia; 
            div_botao.appendChild(div_col_button);
            div_botao.appendChild(a_item) ;
            div_col.appendChild(div_botao);
            contador=1;
            materia.topicos.forEach(topico => {
                var div_topico = document.createElement('div');
                div_topico.id=topico.id_topico ;
                div_topico.className='card-body hover-div' ;//div-display
                var a_item_ = document.createElement('a'); 
                a_item_.text=contador + " - " +topico.nm_topico; 
                a_item_.setAttribute("href", "/pergunta/"+topico.id_topico);
                a_item_.setAttribute('title', 'Clique e cadastre uma nova pergunta do tópico '+topico.nm_topico);
                var spanElement = document.createElement("span");
                spanElement.textContent = "total de Perguntas: "+topico.total_perguntas;
                spanElement.className="badge badge-primary bg-success"
                spanElement.style.float = "right";
                div_topico.appendChild(a_item_) ;
                div_topico.appendChild(spanElement) ;                
                div_conteudo.appendChild(div_topico);
                contador++;
            });
            var div_aux = document.createElement('div');
            div_aux.className='card-body ' ;

            var botao_topico = document.createElement('button'); 
            botao_topico.id="btn-top-"+materia.id_materia;  
            botao_topico.className="btn btn-outline-info";
            botao_topico.textContent="Novo Tópico"
            botao_topico.style.float="right"
            botao_topico.addEventListener("click", function() {
                document.getElementById("janela").style.display = "block";
                
                document.getElementById("id_materia").options[0].value = materia.id_materia;
                document.getElementById("id_materia").options[0].text = materia.nm_materia;
                document.getElementById("id_materia").options[0].selected = true;
            });
            div_aux.appendChild(botao_topico) 
            div_conteudo.appendChild(div_aux) 
            div_conteudo.className="card-body div-display"
            div_col.appendChild(div_conteudo)             
            ul.appendChild(div_col);
        });
        var div_aux = document.createElement('div');
        div_aux.className='card-body ' ;
        var botao_nova_materia = document.createElement('button'); 
        botao_nova_materia.id="btn-materia" 
        botao_nova_materia.className="btn btn-outline-info";
        botao_nova_materia.textContent="Nova Materia"
        botao_nova_materia.style.float="right"
        botao_nova_materia.addEventListener("click", function() {
            document.getElementById("janela-materia").style.display = "block";            
        });
        div_aux.appendChild(botao_nova_materia) 
        ul.appendChild(div_aux) 
    })
    .catch(error => {
      //console.error('Erro ao receber dados do servidor:', error);
    });
}

function f_consultar_topico() { 
    $.get('/topico_con', function(response) { 
        if (response.length > 0) { 
            var div_ativos = document.getElementById("lista-topicos-ativos"); 
            var div_inativos = document.getElementById("lista-topicos-inativos"); 
            div_ativos.innerHTML = ''; 
            div_inativos.innerHTML = '';
            response.forEach(function(topico){ 
                var div_col = document.createElement('div'); 
                var div_card = document.createElement('div'); 
                div_col.className='col card-body' ;
                div_card.className='col' ;
                var li = document.createElement('div'); 
                li.id=topico.id_materia ;
                li.className='card-body hover-div custom-control custom-checkbox' ;
                var a_item = document.createElement('a'); 
                a_item.href='topicos' ;
                a_item.text=topico.id_materia + " - " +topico.nm_topico; 
                var checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = "top-"+topico.id_topico;
                checkbox.name = topico.id_topico+"-"+topico.nm_topico;
                             
                checkbox.className='custom-control-input';
                var label = document.createElement('label');
                label.htmlFor = "top-"+topico.id_topico; 
                label.className="custom-control-label"  
                var spanElement = document.createElement("span");
                spanElement.textContent =topico.total_perguntas;
                if (topico.total_perguntas>0){
                    checkbox.checked = true;  
                    spanElement.className="badge badge-primary bg-success";
                }else{
                    spanElement.className="badge badge-primary bg-danger";
                }
                spanElement.style.float = "right";
                
                checkbox.addEventListener('change', function(event) {
                    f_filtro_perguntas(this);
                });
                label.appendChild(document.createTextNode(topico.nm_topico));
                li.appendChild(checkbox) 
                li.appendChild(label) 
                li.appendChild(spanElement) 
                div_card.appendChild(li) 
                //div_col.appendChild(li) 
                if (topico.total_perguntas>0){
                    div_ativos.appendChild(div_card); 
                }else{
                    div_inativos.appendChild(div_card); 
                }
            }); 
        } else { 
            $('#lista-topicos').append('Nenhum tópico cadastrado.'); 
        } 
    }); 
}

// Topicos e Perguntas Filtro
function f_consultar_topico_perguntas() { 
    $.get('/consultaTodasPerguntas', function(response) { 
        if (response.length > 0) { 
            var ul = document.getElementById("lista-perguntas-topicos"); 
            ul.innerHTML = ''; 
            ul.id="lista-perguntas-topicos" 
            response.forEach(function(topico){ 
                var div_col = document.createElement('div'); 
                var div_card = document.createElement('div'); 
                div_col.className='card-body' 
                div_card.className='card hover-div ' 
                var li = document.createElement('div'); 
                li.id=topico.id_pergunta
                li.className='card-body' 
                li.textContent =topico.pergunta
                var a_item = document.createElement('a'); 
                a_item.href='topicos' 
                a_item.text=topico.nm_topico; 
                div_col.style.display='block';
                div_col.setAttribute('data-name', "pergu_"+topico.id_topico + "-" +topico.nm_topico);
                var spanElement = document.createElement("span");
                spanElement.textContent = topico.nm_topico +" de "+topico.nm_materia;
                spanElement.className="text-wrap badge badge-primary bg-success "
                spanElement.style.float = "right";
                li.appendChild(spanElement) 
                contador=1
                var div_conteudo_body = document.createElement('div');
                //div_conteudo_body.className='card-body ' ;
                topico.alternativas.forEach(alternativa => {
                    var div_conteudo = document.createElement('div');
                    //div_conteudo.className='' ;
                    var div_topico = document.createElement('div');
                    div_topico.id=alternativa.id_alternativa ;
                    div_topico.className='card-body hover-div ' ;//div-display
                    var a_item_ = document.createElement('a'); 
                    a_item_.text=contador + " - " +alternativa.alternativa; 
                    //a_item_.className='text-wrap '
                    //a_item_.setAttribute("href", "/perguntas/"+topico.id_topico);
                    div_topico.appendChild(a_item_) ;
                    div_conteudo.appendChild(div_topico);
                    if(alternativa.correta){
                        a_item_.style.color="green"
                    }else{
                        a_item_.style.color="red"
                    }
                    div_conteudo_body.appendChild(div_conteudo);
                    contador++;
                    
                    
                });
                li.appendChild(div_conteudo_body); 
                div_card.appendChild(li);    
                div_col.appendChild(div_card);            
                ul.appendChild(div_col); 
            }); 
        } else { 
            $('#lista-topicos').append('Nenhum tópico cadastrado.'); 
        } 
    }); 
}
function f_filtro_perguntas(checkbox){
    var divs = document.querySelectorAll('div[data-name="pergu_' + checkbox.name + '"]');
    if (divs){
        divs.forEach(function(div) {
            //console.log("mudei",div.style.display,div.id,divs)
            div.style.display = checkbox.checked ? 'block' : 'none';
            //console.log("ficou",div.style.display,div.id)
        });
    }
    f_consultarDivsPerguntasAtivas();
}
function f_consultarDivsPerguntasAtivas(){
    var divs = document.querySelectorAll('[id^="pergunta_"]:not([style*="display: none"])');
    //console.log(divs.length,divs)
    if (divs.length>0){
        $('#mensagem_index').text(''); 
    }else{
        $('#mensagem_index').text('Não há perguntas para exibir, verifique os filtros ou atualize a página'); 
    }
}

function expandirDiv(element) {
    _idDiv_ = element.getAttribute('data-name');
    var divCadastroTopico=document.getElementById(_idDiv_);
    element.textContent="-"
    if (divCadastroTopico.style.display == "block"){
        divCadastroTopico.style.display = "none";
        element.textContent="+"
    }else{
        divCadastroTopico.style.display = "block";
    }
}
  // Função para fechar a "janela"
function fecharJanela() {
    document.getElementById("janela").style.display = "none";
}
function fecharJanelaMateria() {
    document.getElementById("janela-materia").style.display = "none";
}