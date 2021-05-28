import Router from 'vue-router'
import Test from '@/components/Tests/Test'
import AddServer from '@/components/Server/AddServer'
import DeleteServer from '@/components/Server/DeleteServer'
import EditAlert from '@/components/Server/EditAlert'

import ServerList from '@/components/Dashboard/ServerList'
import CardList from '@/components/Dashboard/CardList'
import Details from '@/components/Systems/Details'

import Bios from '@/components/Systems/Bios'
import Logs from '@/components/Systems/Logs'
import Memory from '@/components/Systems/Memory'
import Processors from '@/components/Systems/Processors'
import Chassis from '@/components/Systems/Chassis'


import Charts from '@/components/Charts/Chart'



export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name:'ServerList',
      component: ServerList,
    },
    {
      path: '/ServerList',
      name:'ServerList',
      component: ServerList,
    },
    {
      path: '/dashboard',
      name:'Dashboard',
      component: CardList,
    },
    {
      path: '/test',
      name:'test',
      component: Test,
    },
    {
      path: '/AddServer',
      name:'AddServer',
      component: AddServer,
    },    
    {
      path: '/DeleteServer',
      name:'DeleteServer',
      component: DeleteServer,
    },    
    // 정보 페이지
    {
      path: '/dashboard/:id/details',
      name:'Details',
      component: Details,
      props: route => ({
        id: String(route.params.id)
      }),
    },
   

    {
      path: '/dashboard/:id/bios',
      name:'bios',
      component: Bios,
      props: route => ({
        id: String(route.params.id)
      }),
    },
    {
      path: '/dashboard/:id/processors',
      name:'processors',
      component: Processors,
      props: route => ({
        id: String(route.params.id)
      }),
    },
    {
      path: '/dashboard/:id/memory',
      name:'memory',
      component: Memory,
      props: route => ({
        id: String(route.params.id)
      }),
    },
    {
      path: '/dashboard/:id/logs',
      name:'logs',
      component: Logs,
      props: route => ({
        id: String(route.params.id)
      }),
    },
    {
      path: '/dashboard/:id/Chassis',
      name:'Chassis',
      component: Chassis,
      props: route => ({
        id: String(route.params.id)
      }),
    },
    
    {
      path: '/dashboard/:id/Charts',
      name:'Charts',
      component: Charts,
      props: route => ({
        id: String(route.params.id)
      }),
    },
    {
      path: '/dashboard/:id/EditAlert',
      name:'EditAlert',
      component: EditAlert,
      props: route => ({
        id: String(route.params.id)
      }),
    },
    
  ]
})
