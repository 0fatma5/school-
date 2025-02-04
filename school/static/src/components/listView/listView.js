/* @odoo-module */
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListViewAction extends Component {
    static template = "school.ListView";

    setup() {
        // Initialize the state
        this.state = useState({
            records: []  // Store the records here
        });

        // Use the 'orm' and 'rpc' services
        this.orm = useService("orm");
        this.rpc = useService("rpc");

        // Load records
        this.loadRecords();
    }

    // Function to load records via rpc
    async loadRecords() {
        try {
            // Make an RPC call to fetch the data
            const result = await this.rpc("web/dataset/call_kw",{
                model: 'school',
                method: 'search_read',
                args: [[]],
                kwargs: { fields: ['id', 'name', 'location', 'Principal_Name'] }
            });

            // Assign the fetched records to the component's state
            this.state.records = result;
        } catch (error) {
            console.error('Error loading records:', error);
        }
    }
}

registry.category("actions").add("school.action_list_view", ListViewAction);
