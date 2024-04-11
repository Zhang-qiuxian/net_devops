<template>
    <d-table :data="baseTableData" style="width: 100%">
        <d-column field="firstName" header="First Name"></d-column>
        <d-column field="lastName" header="Last Name"></d-column>
        <d-column field="gender" header="Gender"></d-column>
        <d-column field="date" header="Date of birth"></d-column>
    </d-table>
</template>

<script setup>
import { ref } from 'vue';


const baseTableData = ref([
    {
        firstName: 'Mark',
        lastName: 'Otto',
        date: '1990/01/11',
        gender: 'Male',
    },
    {
        firstName: 'Jacob',
        lastName: 'Thornton',
        gender: 'Female',
        date: '1990/01/12',
    },
    {
        firstName: 'Danni',
        lastName: 'Chen',
        gender: 'Male',
        date: '1990/01/13',
    },
    {
        firstName: 'green',
        lastName: 'gerong',
        gender: 'Male',
        date: '1990/01/14',
    },
]);

</script>