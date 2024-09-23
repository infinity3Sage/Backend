document.addEventListener('DOMContentLoaded', function() {
    const modulosField = document.querySelectorAll('#id_modulos input[type="checkbox"]');
    const submodulosField = document.querySelector('#id_submodulos');
    const empresaId = document.querySelector('input[name="id"]').value;

    if (!modulosField.length || !submodulosField) {
        console.error('No se encontraron los campos de módulos o submódulos.');
        return;
    }

    function fetchSubmodulos() {
        const selectedModulos = Array.from(modulosField)
            .filter(input => input.checked)
            .map(input => input.value);

        if (selectedModulos.length === 0) {
            submodulosField.innerHTML = '';
            return;
        }

        fetch(`/admin/empresa/empresa/filter-submodulos/?modulos_ids=${selectedModulos.join(',')}&empresa_id=${empresaId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                submodulosField.innerHTML = '';
                data.forEach(submodulo => {
                    const div = document.createElement('div');
                    const label = document.createElement('label');
                    const input = document.createElement('input');
                    input.type = 'checkbox';
                    input.name = 'submodulos';
                    input.value = submodulo.id;
                    input.id = `id_submodulos_${submodulo.id}`;
                    input.dataset.moduloId = submodulo.modulo_id;
                    if (submodulo.selected) {
                        input.checked = true;
                    }
                    label.htmlFor = input.id;
                    label.textContent = ` ${submodulo.nombre}`;
                    div.appendChild(input);
                    div.appendChild(label);
                    submodulosField.appendChild(div);
                });
            })
            .catch(error => {
                console.error('Error fetching submodules:', error);
                alert('Error fetching submodules. Please try again later.');
            });
    }
    fetchSubmodulos();

    modulosField.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
          
            if (!this.checked) {
                var modulo_id = this.value; 

                document.querySelectorAll('input[name="submodulos"]').forEach(function(submoduloCheckbox) {
                    var submodulo_modulo_id = submoduloCheckbox.getAttribute('data-modulo-id');

                    if (submodulo_modulo_id === modulo_id) {
                        submoduloCheckbox.checked = false;
                    }
                });
            }
            fetchSubmodulos();
        });
    });
});
