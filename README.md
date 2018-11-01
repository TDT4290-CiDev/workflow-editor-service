# WorkflowEditorService

This service provides endpoints for creating, reading, updating and deleting workflows.

# Structure of a Workflow

A workflow is defined in JSON with the following format:

```json
{
	"start_block": "1",
	"blocks": {
		"1": {
			"type": "action",
			"name": "send_email",
			"params": {
				"address": "mail@example.com",
				"subject": "Test mail",
				"body": "This is a test mail."
			},
			"save_outputs": {},
			"next_block": "2"
		},
		"2": {
			"type": "branch",
			"condition": "'{outputs.response}' == 'mail_sent'",
			"next_block": [
				"3", "4"
			]
		},
		"3": {
			"type": "action",
			"name": "update_user_info",
			"params": {
				"first_name": "John",
				"last_name": "Doe"
			},
			"save_outputs": {
				"first_name": "user.first_name"
			},
			"next_block": "-1"
		},
		"4": {
			"type": "action",
			"name": "post_on_twitter",
			"params": {
				"content": "This is a Twitter post by {store.user.first_name}"
			},
			"save_outputs": [],
			"next_block": "-1"
		}
	},
	"inputs": {
		"input1": {
			"description": "The first input",
			"type": "string"
		},
		"input2": {
			"description": "The second input",
			"type": "integer"
		}
	}
}
```

The most central element is the `blocks` object, which enumerates all the blocks in the workflow. It is effectively a
list, but is implemented as an object mapping IDs to blocks to avoid problems with the indexing changing when blocks are
removed. The blocks are organized in a flat structure to allow effective indexing when resuming execution of a case.

There are several types of blocks, defined by the `type` parameter. `action` blocks correspond to an endpoint on the 
`WorkflowBlockService` - see blocks 1, 3 and 4 above. For these blocks, the following parameters must be set:

*   `name`: The name of the block that should be called.
*   `params`: Params that should be passed to the block. These can either be given as constant values, or variable
values from either the store or output from the previous block in the workflow (or a combination). In the latter case, 
dot notation is used, and the variable name is written within curly braces. `store` gives access to data from the store, 
and `outputs` gives access to outputs from the previous block. For example, `store.user.first_name` fetches the 
`first_name` property of the `user` object in the `store`.
*   `save_outputs`: A mapping of outputs from the block to locations in the store. Any outputs that are present in
`save_outputs` will be written to the store for persistent saving, overwriting anything that was previously in the same
location. For example, `first_name: user.first_name` saves the `first_name` output to the `first_name` property of the
`user` object in the `store`.
*   `next_block`: A pointer to the ID of the block that should be executed after the given block. If `'-1'`, the block
is terminal.

`branch` blocks allow binary branching, providing the flow control of the workflow. They have two parameters:

*   `condition`: A string defining the condition controlling the branch. The string uses Python syntax, which means
that the available operators should be familiar for most programmers. Examples are `==`, which checks for equality,
and `>`, which checks if one operator is larger than the other. Variables from either previous output or store can be
inserted in the same way as for `params` in the `action` blocks.
*   `next_block`: A list giving the next block as decided by the state of the condition. If the condition evaluates to
`true`, the first block is selected; otherwise, the second block is selected. Can also be `'-1'` to optionally
terminate the workflow.

`start_block` is a simple reference to the first block that will be executed in the workflow. Usually, this will also
be the first block in the `blocks` list, but this is left up to the user.

`inputs` enumerates the inputs required by the workflow. These must at minimum cover the inputs required by the first
block in the workflow.
