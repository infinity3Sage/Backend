// usuarios/static/usuarios/js/filter_submodulos.js

document.addEventListener('DOMContentLoaded', function() {
    const modulosField = document.querySelectorAll('#id_modulos input[type="checkbox"]');
    const submodulosField = document.querySelector('#id_submodulos');

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

        const empresaId = document.querySelector('#id_empresa').value;

        fetch(`/admin/user/useraccount/filter-submodulos/?empresa_id=${empresaId}&modulos_ids=${selectedModulos.join(',')}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error HTTP! Estado: ${response.status}`);
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
                    label.htmlFor = input.id;
                    label.textContent = ` ${submodulo.nombre}`;
                    div.appendChild(input);
                    div.appendChild(label);
                    submodulosField.appendChild(div);
                });
            })
            .catch(error => {
                console.error('Error al obtener submódulos:', error);
                alert('Error al obtener submódulos. Por favor, inténtelo de nuevo más tarde.');
            });
    }
    fetchSubmodulos();

    modulosField.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (!this.checked) {
                // Si el checkbox de módulo se desmarca, ocultar los submódulos asociados
                const moduloId = this.value;

                document.querySelectorAll('input[name="submodulos"]').forEach(submoduloCheckbox => {
                    if (submoduloCheckbox.dataset.moduloId === moduloId) {
                        submoduloCheckbox.closest('div').style.display = 'none';
                    }
                });
            } else {
                // Si el checkbox de módulo se marca, mostrar los submódulos asociados
                fetchSubmodulos();
            }
        });
    });
});
