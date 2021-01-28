from Objects.TestBedObject import Node, Shard, Beacon, Staker

addr = "51.79.76.38"

full_node = Node(address=addr, rpc_port=8334, ws_port=18334, node_name='fullnode-testnet')

beacon = Beacon([
    Node(address=addr, rpc_port=9335, node_name='beacon0'),
    Node(address=addr, rpc_port=9336, node_name='beacon1'),
    Node(address=addr, rpc_port=9337, node_name='beacon2'),
    Node(address=addr, rpc_port=9338, node_name='beacon3'),
])

shard_list = [Shard([Node(address=addr, rpc_port=9339, ws_port=19339, node_name='shard0-0'),
                     Node(address=addr, rpc_port=9340, ws_port=19340, node_name='shard0-1'),
                     Node(address=addr, rpc_port=9341, ws_port=19341, node_name='shard0-2'),
                     Node(address=addr, rpc_port=9342, ws_port=19342, node_name='shard0-3'),
                     ]),
              Shard([Node(address=addr, rpc_port=9343, ws_port=19343, node_name='shard1-0'),
                     Node(address=addr, rpc_port=9344, ws_port=19344, node_name='shard1-1'),
                     Node(address=addr, rpc_port=9345, ws_port=19345, node_name='shard1-2'),
                     Node(address=addr, rpc_port=9346, ws_port=19346, node_name='shard1-3'),
                     ]),
              Shard([Node(address=addr, rpc_port=9347, ws_port=19347, node_name='shard2-0'),
                     Node(address=addr, rpc_port=9348, ws_port=19348, node_name='shard2-1'),
                     Node(address=addr, rpc_port=9349, ws_port=19349, node_name='shard2-2'),
                     Node(address=addr, rpc_port=9350, ws_port=19350, node_name='shard2-3'),
                     ]),
              Shard([Node(address=addr, rpc_port=9351, ws_port=19351, node_name='shard3-0'),
                     Node(address=addr, rpc_port=9352, ws_port=19352, node_name='shard3-1'),
                     Node(address=addr, rpc_port=9353, ws_port=19353, node_name='shard3-2'),
                     Node(address=addr, rpc_port=9354, ws_port=19354, node_name='shard3-3'),
                     ])
              ]

staker_list = Staker([
    Node(address=addr, rpc_port=10335, node_name='staker0'),
    Node(address=addr, rpc_port=10336, node_name='staker1'),
    Node(address=addr, rpc_port=10337, node_name='staker2'),
    Node(address=addr, rpc_port=10338, node_name='staker3'),
    Node(address=addr, rpc_port=10339, node_name='staker4'),
    Node(address=addr, rpc_port=10340, node_name='staker5'),
    Node(address=addr, rpc_port=10341, node_name='staker6'),
    Node(address=addr, rpc_port=10342, node_name='staker7'),
    Node(address=addr, rpc_port=10343, node_name='staker8'),
    Node(address=addr, rpc_port=10344, node_name='staker9'),
    Node(address=addr, rpc_port=10345, node_name='staker10'),
    Node(address=addr, rpc_port=10346, node_name='staker11'),
    Node(address=addr, rpc_port=10347, node_name='staker12'),
    Node(address=addr, rpc_port=10348, node_name='staker13'),
    Node(address=addr, rpc_port=10349, node_name='staker14'),
    Node(address=addr, rpc_port=10350, node_name='staker15'),
    Node(address=addr, rpc_port=10351, node_name='staker16'),
    Node(address=addr, rpc_port=10352, node_name='staker17'),
    Node(address=addr, rpc_port=10353, node_name='staker18'),
    Node(address=addr, rpc_port=10354, node_name='staker19'),
    Node(address=addr, rpc_port=10355, node_name='staker20'),
    Node(address=addr, rpc_port=10356, node_name='staker21'),
    Node(address=addr, rpc_port=10357, node_name='staker22'),
    Node(address=addr, rpc_port=10358, node_name='staker23'),
    Node(address=addr, rpc_port=10359, node_name='staker24'),
    Node(address=addr, rpc_port=10360, node_name='staker25'),
    Node(address=addr, rpc_port=10361, node_name='staker26'),
    Node(address=addr, rpc_port=10362, node_name='staker27'),
    Node(address=addr, rpc_port=10363, node_name='staker28'),
    Node(address=addr, rpc_port=10364, node_name='staker29'),
    Node(address=addr, rpc_port=10365, node_name='staker30'),
    Node(address=addr, rpc_port=10366, node_name='staker31'),
    Node(address=addr, rpc_port=10367, node_name='staker32'),
    Node(address=addr, rpc_port=10368, node_name='staker33'),
    Node(address=addr, rpc_port=10369, node_name='staker34'),
])
