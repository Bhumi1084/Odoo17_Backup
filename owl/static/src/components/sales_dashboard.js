/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, useRef, onMounted } = owl

export class OwlSalesDashboard extends Component {
    setup(){
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/chart.js/4.4.0/chart.umd.min.js")
        })

        onMounted(()=>{
            const data = [
                { year: 2010, count: 10 },
                { year: 2011, count: 20 },
                { year: 2012, count: 15 },
                { year: 2013, count: 25 },
                { year: 2014, count: 22 },
                { year: 2015, count: 30 },
                { year: 2016, count: 28 },
            ];

             new Chart(
                this.chartRef.el,
                {
                  type: 'bar',
                  data: {
                    labels: data.map(row => row.year),
                    datasets: [
                      {
                        label: 'Acquisitions by year',
                        data: data.map(row => row.count)
                      }
                    ]
                  }
                }
             );
        })
    }
}

OwlSalesDashboard.template = "owl.OwlSalesDashboard"
OwlSalesDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add("owl.sales_dashboard", OwlSalesDashboard)