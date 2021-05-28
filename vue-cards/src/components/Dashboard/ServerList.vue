<template>
    <div class="table-outline">
      <MainHeader class="product"/>
      
      <button class="serverButton"
      @click="[isModalViewed = true, server = 'AddServer']">Add Server</button>

      <button class="serverButton"
      @click="[isModalViewed = true, server='DeleteServer']">Delete Server</button>

      <table class="table table-striped" id="summary-table" cellspacing="0" width="100%">
        <thead>
          <tr>    
            <th>ip</th>
            <th>Id</th>
            <th>Name</th>
            <th>SystemType</th>
            <th>AssetTag</th>
            <th>Manufacturer</th>
            <th>Model</th>
            <th>SKU</th>
            <th>SerialNumber</th>
            <th>PartNumber</th>
            <th>Description</th>
            <th>UUID</th>
            <th>HostName</th>
            <th>Status</th>
            <th>IndicatorLED</th>
            <th>PowerState</th>
            <th>Boot</th>
            <th>TrustedModules</th>
            <th>Oem</th>
            <th>BiosVersion</th>
            <th>ProcessorSummary</th>
            <th>MemorySummary</th>
            <th>상세보기</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>

      <MainModal 
          v-if="isModalViewed" 
          @close-modal="[isModalViewed = false, refreshAll()]"> 
          <MainContent :server="server"/> 
      </MainModal> 
  </div>

</template>

<script>
import { mapGetters } from 'vuex'
import MainHeader from '@/components/Main/MainHeader'
//Bootstrap and jQuery libraries
import 'jquery/dist/jquery.min.js';
//Datatable Modules
import "datatables.net-dt/js/dataTables.dataTables"
import "datatables.net-dt/css/jquery.dataTables.min.css"
import 'datatables.net-bs';
// import jsZip from 'jszip';
import 'datatables.net-buttons-bs';
import 'datatables.net-buttons/js/buttons.colVis.min';
import 'datatables.net-buttons/js/dataTables.buttons.min';
import 'datatables.net-buttons/js/buttons.flash.min';
import 'datatables.net-buttons/js/buttons.html5.min';

import MainModal from '@/components/Main/MainModal'
import MainContent from '@/components/Main/MainContent'
// This line was the one missing
// window.JSZip = jsZip;

import $ from 'jquery'; 

export default {
	name: 'code-list',

  components: {
    MainHeader,
    MainContent,
    MainModal
  },

  computed: {
    ...mapGetters('dashboard', [
      'dashboard'
    ]),
  },
  methods: {
    refreshAll() {
        // 새로고침
        this.$router.go();
    }
  },

  mounted() {
    // this.$store.dispatch('dashboard/fetchDashboard')
    this.id = this.$route.params.id 

    $ ( '#table' ).ready(function() {
    $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/api/dashboard',
        mimeType: 'json',
        success: function(data) {
            $.each(data, function(i, data) {
                var body = "<tr>";
                body    += "<td><a href=\"https://" + data.ip + "\">" + data.ip + "</a></td>";
                body    += "<td>" + data.Id + "</td>";
                body    += "<td>" + data.Name + "</td>";
                body    += "<td>" + data.SystemType + "</td>";
                body    += "<td>" + data.AssetTag + "</td>";
                body    += "<td>" + data.Manufacturer + "</td>";
                body    += "<td>" + data.Model + "</td>";
                body    += "<td>" + data.SKU + "</td>";
                body    += "<td>" + data.SerialNumber + "</td>";
                body    += "<td>" + data.PartNumber + "</td>";
                body    += "<td>" + data.Description + "</td>";
                body    += "<td>" + data.UUID + "</td>";
                body    += "<td>" + data.HostName + "</td>";
                body    += "<td>" + JSON.stringify(data.Status.State) + "</td>";
                body    += "<td>" + data.IndicatorLED + "</td>";
                body    += "<td>" + data.PowerState + "</td>";
                body    += "<td>" + JSON.stringify(data.Boot) + "</td>";
                body    += "<td>" + JSON.stringify(data.TrustedModules) + "</td>";
                body    += "<td>" + JSON.stringify(data.Oem) + "</td>";
                body    += "<td>" + data.BiosVersion + "</td>";
                body    += "<td>" + JSON.stringify(data.ProcessorSummary.Model) + "<br>Status: " + JSON.stringify(data.ProcessorSummary.Status.HealthRollup) + "</td>";
                body    += "<td>" + JSON.stringify(data.MemorySummary.TotalSystemMemoryGiB) + " GiB<br>Status: " + JSON.stringify(data.MemorySummary.Status.HealthRollup) + "</td>";
                // body    += "<td><button class=\"serverButton\" @click=\"isModalViewed = true\">상세보기</button></td>";
                body    += "<td><a href=\"/dashboard/" + data.ip + "/details\"><button >상세보기</button></a></td>";

                body    += "</tr>";
                // console.log(body)
                $( "#summary-table tbody" ).append(body);
            });
            
            /*DataTables instantiation.*/
            $( "#summary-table" ).DataTable(
              {
                  // dom: 'Bfrtip',
                  dom: 'C<"clear">RZlBfrtip',
                  buttons: {
                    buttons: [
                      'copy', 'excel', 'pdf', 'colvis'
                    ],
                    dom: {
                      button: {
                        tag: "button",
                        className: "button"
                      },
                      buttonLiner: {
                        tag: null
                      }
                    }

                  },
                    

                  columnDefs :
                  [
                    // {width: "10%", targets : [0, 1, 15] },
                    {width: "5.38%", targets : '_all' },
                    { "targets": [ 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, ], "visible": false }
                    // {orderable : false, targets : [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]} // 자동정렬하지 못하게(상단)
                  ],
                  
                  lengthMenu : [[5, 10, 25, -1], [5, 10, 25, 'all']], // show entries 메뉴 설정(앞 [] 보여줄 개수, 뒤 [] 표시할 문자)
                  pageLength : 5, // 기본 보여줄 row 개수 설정, 메뉴와 일치할 경우 메뉴가 자동으로 세팅된다.
                  language : {
                    info : '총  _TOTAL_ 개의 행 중 _START_ 행 부터 _END_ 행 까지',
                    infoEmpty : '데이터가 없습니다.',
                    emptyTable : '데이터가 없습니다.',
                    thousands : ',',
                    lengthMenu : '총 _MENU_ 행씩 보기',
                    loadingRecords : '열심히 불러오는 중',
                    processing : '열심히 동작 중',
                    zeroRecords : '검색 결과 없음',
                    paginate : {
                          first : '처음',
                          last : '끝',
                          next : '다음',
                          previous : '이전'
                    },
                    search : '검색 '
                    }
              } 
            );
            // $('#summary-table tbody').on('click', 'tr', function () {
            //     console.log(table.row(this).data()[0].split(">")[1].split("<")[0]);
            //     $('#btn').click()
            // });
            // $('#summary-table tbody').on('hover', 'tr', function(){
            //     $(document).find('tr').removeClass("dtSelected");
            //     $(table.row(this).selector.rows).addClass("dtSelected");
            // });
        },
        error: function() {
            alert('Fail!');
        }
    });
    });


  },

  data: function() {
    return {
        // users:[]
        isModalViewed: false,
        server: ''
    }
  },


}
</script>


<style>
    .table {
        width: 100%;
        margin: 0 auto;
        border-collapse: collapse;
        text-align: center;
    }

    td {
      /* border: 0.3px solid #e3e3e3; */
      /* height: 40px; */
      box-shadow: 0px 1px 0px rgba(0, 0, 0, 0.35);
    }


    .serverButton {
      height: 30px;
      margin: 10px;
      background: var(--button-bg-color);
      color: var(--button-color);  
      
      border: none;
      border-radius: 10px;
        
      display: inline-block;
      width: 110px;
      text-align: center;
      
      box-shadow: 3px 5px 5px 3px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
      
      cursor: pointer;
    }

    .button {
      height: 30px;
      background: var(--button-bg-color);        
      
      border: none;
      border-radius: 10px;

      margin: 5px;

      display: inline-block;
      width: 110px;
      text-align: center;
      
      box-shadow: 3px 5px 5px 3px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
      
      cursor: pointer;
    }

    table#summary-table.dataTable tbody tr:hover 
    {
        background-color: #4B96E7;
        /* cursor: pointer; */
    }

    table#summary-table.dataTable tbody tr:hover > .sorting_1 
    {
        background-color: #4B96E7;
        /* cursor: pointer; */
    }
</style>