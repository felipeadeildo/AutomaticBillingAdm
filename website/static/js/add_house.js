const cep_input = document.getElementById('cep');
const estado_input = document.getElementById("estado");
const estado_label = document.getElementById("estado_label")
const cidade_input = document.getElementById("cidade");
const cidade_label = document.getElementById("cidade_label");
const logradouro_input = document.getElementById("endereco");
const logradouro_label = document.getElementById("endereco_label");
const bairro_input = document.getElementById("bairro");
const bairro_label = document.getElementById("bairro_label");
const complemento_input = document.getElementById("complemento");
const complemento_label = document.getElementById("complemento_label");


// evento que é excutado onChange da referencia pra cep_input :D
cep_input.addEventListener('change', () => {
    const cep = cep_input.value.replace("/\D/g", ''); // obtém valor do cep e deixa muda tudo que não for inteiro para ''
    if (cep.length == 8) {
        fetch(`https://viacep.com.br/ws/${cep}/json`)
            .then(response => response.json())
            .then(data => {
                // preenche os campos com os dados da resposta da API
                if (data.uf != "") {
                    estado_input.value = data.uf;
                    estado_label.classList.add("active");
                }
                cidade_input.value = data.localidade;
                cidade_label.classList.add("active");
                logradouro_input.value = data.logradouro;
                logradouro_label.classList.add("active");
                complemento_input.value = data.complemento;
                complemento_label.classList.add("active");
                bairro_input.value = data.bairro;
                bairro_label.classList.add("active");
            })
            .catch(error => console.error(error));
    }
});