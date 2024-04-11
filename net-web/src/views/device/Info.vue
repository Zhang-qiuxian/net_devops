<template>
    <div>
        <div class="mb-2">
            <d-button @click="handleClick" class="mr-1">Get CheckedRows</d-button>
            <d-button @click="insertRow" class="mr-1">Insert Row</d-button>
            <d-button @click="deleteRow" class="mr-1">Delete Row</d-button>
            <d-button @click="toggleRow" class="mr-1">Toggle Row</d-button>
        </div>
        <d-table ref="tableRef" :data="data" :row-key="(item) => item.id" @cell-click="onCellClick"
            @row-click="onRowClick" @check-change="checkChange" @check-all-change="checkAllChange">
            <d-column type="checkable" width="40" :checkable="checkable" reserve-check></d-column>
            <d-column field="firstName" header="First Name" width="200"></d-column>
            <d-column field="lastName" header="Last Name" width="200" resizeable min-width="150" max-width="250"
                @resize-start="onResizeStart" @resizing="onResizing" @resize-end="onResizeEnd"></d-column>
            <d-column field="gender" header="Gender"></d-column>
            <d-column field="date" header="Date of birth"></d-column>
        </d-table>
    </div>
</template>

<script setup>
import { ref } from 'vue';


const tableRef = ref();
const data = ref([
    {
        id: '0',
        firstName: 'po',
        lastName: 'Lang',
        gender: 'Male',
        date: '1990/01/15',
    },
    {
        id: '1',
        firstName: 'john',
        lastName: 'Li',
        gender: 'Female',
        date: '1990/01/16',
    },
    {
        id: '2',
        firstName: 'peng',
        lastName: 'Li',
        gender: 'Male',
        date: '1990/01/17',
    },
    {
        id: '3',
        firstName: 'Dale',
        lastName: 'Yu',
        gender: 'Female',
        date: '1990/01/18',
    },
]);
const handleClick = () => {
    console.log(tableRef.value.store.getCheckedRows());
};
const onCellClick = (params) => {
    console.log('cell-click', params);
};
const onRowClick = (params) => {
    console.log('row-click', params);
};

const checkChange = (checked, row, selection) => {
    console.log('checked row:', checked, row, selection);
};

const checkAllChange = (checked, selection) => {
    console.log('checked:', checked, selection);
};

const toggleRow = () => {
    tableRef.value.store.toggleRowSelection(data.value[0]);
};

const checkable = (row, rowIndex) => {
    return row.lastName === 'Li' || false;
};

const insertRow = () => {
    data.value.push({
        id: `${data.value.length}`,
        firstName: 'Jeff',
        lastName: 'You',
        gender: 'Male',
        date: '1989/05/19',
    });
};

const deleteRow = () => {
    data.value.splice(0, 1);
};

const onResizeStart = (e) => {
    console.log('resize start', e);
};

const onResizing = (e) => {
    console.log('resizing', e);
};

const onResizeEnd = (e) => {
    console.log('resize end', e);
};

</script>