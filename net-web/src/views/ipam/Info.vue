<template>
    <d-table :data="tableDataFixedColumn" table-layout="auto">
        <d-column field="idNo" header="ID Card Number" fixed-left="0px"></d-column>
        <d-column field="firstName" header="First Name"></d-column>
        <d-column field="lastName" header="Last Name"></d-column>
        <d-column field="gender" header="Gender"></d-column>
        <d-column field="date" header="Date of birth"></d-column>
        <d-column field="address" header="Address"></d-column>
        <d-column field="occupation" header="Occupation"></d-column>
        <d-column field="occupation" header="Occupation"></d-column>
        <d-column field="occupation" header="Occupation"></d-column>
        <d-column field="occupation" header="Occupation" fixed-right="0px"></d-column>
    </d-table>
</template>

<script setup>
import { ref,computed } from 'vue';


const tableDataFixedColumn = ref([
    {
        firstName: 'po',
        lastName: 'Lang',
        gender: 'Male',
        date: '1990/01/15',
        address: 'Shenzhen Guangdong',
        occupation: 'Worker',
        idNo: '2000**********9999',
    },
    {
        firstName: 'john',
        lastName: 'Li',
        gender: 'Female',
        date: '1990/01/16',
        address: 'Shenzhen Guangdong',
        occupation: 'Worker',
        idNo: '2000**********9999',
    },
    {
        firstName: 'peng',
        lastName: 'Li',
        gender: 'Male',
        date: '1990/01/17',
        address: 'Shenzhen Guangdong',
        occupation: 'Worker',
        idNo: '2000**********9999',
    },
    {
        firstName: 'Dale',
        lastName: 'Yu',
        gender: 'Female',
        date: '1990/01/18',
        address: 'Shenzhen Guangdong',
        occupation: 'Worker',
        idNo: '2000**********9999',
    },
]);

const filterList = computed(() =>
    tableDataFixedColumn.value.map((item) => ({ name: `${item.firstName} ${item.lastName}`, value: item.firstName }))
);


</script>