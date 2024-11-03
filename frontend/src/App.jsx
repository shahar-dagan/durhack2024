import React, { useCallback, useState } from 'react';
import axios from 'axios';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Handle,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const initialNodes = [
  { id: 'button-1', position: { x: 0, y: 0 }, data: { label: 'Button Node 1' }, type: 'buttonNode' },
  { id: 'action-1', position: { x: 0, y: 100 }, data: { label: 'Action Node 1' }, type: 'actionNode' },
];
const initialEdges = [{ id: 'e1-2', source: 'button-1', target: 'action-1', label: 'Edge Label' }];

function ButtonNode({ id, data, isConnectable }) {
  const [isEditing, setIsEditing] = useState(false);
  const [label, setLabel] = useState(data.label);

  const onDoubleClick = () => setIsEditing(true);
  const onBlur = () => {
    data.onChangeLabel(id, label);
    setIsEditing(false);
  };

  return (
    <div onDoubleClick={onDoubleClick} style={{ padding: '10px', backgroundColor: '#f0f0f0', borderRadius: '5px' }}>
      {isEditing ? (
        <input
          value={label}
          onChange={(e) => setLabel(e.target.value)}
          onBlur={onBlur}
          autoFocus
        />
      ) : (
        <div>{label}</div>
      )}
      <Handle type="target" position="top" isConnectable={isConnectable} />
      <Handle type="source" position="bottom" isConnectable={isConnectable} />
    </div>
  );
}

function ActionNode({ id, data, isConnectable }) {
  const [isEditing, setIsEditing] = useState(false);
  const [label, setLabel] = useState(data.label);

  const onDoubleClick = () => setIsEditing(true);
  const onBlur = () => {
    data.onChangeLabel(id, label);
    setIsEditing(false);
  };

  return (
    <div onDoubleClick={onDoubleClick} style={{ padding: '10px', backgroundColor: '#e0ffe0', borderRadius: '5px' }}>
      {isEditing ? (
        <input
          value={label}
          onChange={(e) => setLabel(e.target.value)}
          onBlur={onBlur}
          autoFocus
        />
      ) : (
        <div>{label}</div>
      )}
      <Handle type="target" position="top" isConnectable={isConnectable} />
      <Handle type="source" position="bottom" isConnectable={isConnectable} />
    </div>
  );
}

function EditableEdge({ id, sourceX, sourceY, targetX, targetY, data, style, markerEnd }) {
  const [isEditing, setIsEditing] = useState(false);
  const [label, setLabel] = useState(data.label);

  const onDoubleClick = () => setIsEditing(true);
  const onBlur = () => {
    data.onChangeLabel(id, label);
    setIsEditing(false);
  };

  return (
    <g>
      <path
        id={id}
        style={style}
        className="react-flow__edge-path"
        d={`M ${sourceX},${sourceY}L ${targetX},${targetY}`}
        markerEnd={markerEnd}
      />
      {isEditing ? (
        <foreignObject x={(sourceX + targetX) / 2 - 50} y={(sourceY + targetY) / 2 - 10} width="100" height="20">
          <input
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            onBlur={onBlur}
            autoFocus
            style={{ width: '100%', fontSize: '12px' }}
          />
        </foreignObject>
      ) : (
        <text
          x={(sourceX + targetX) / 2}
          y={(sourceY + targetY) / 2 - 10}
          onDoubleClick={onDoubleClick}
          style={{ fontSize: '12px', cursor: 'pointer' }}
        >
          {label}
        </text>
      )}
    </g>
  );
}

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge({ ...params, label: 'New Edge' }, eds)),
    [setEdges]
  );

  const addButtonNode = () => {
    const newNode = {
      id: `button-${nodes.filter(node => node.id.startsWith('button')).length + 1}`,
      position: { x: Math.random() * 250, y: Math.random() * 250 },
      data: { label: `Button Node ${nodes.filter(node => node.id.startsWith('button')).length + 1}`, onChangeLabel: handleLabelChange },
      type: 'buttonNode',
    };
    setNodes((nds) => [...nds, newNode]);
  };

  const addActionNode = () => {
    const newNode = {
      id: `action-${nodes.filter(node => node.id.startsWith('action')).length + 1}`,
      position: { x: Math.random() * 250, y: Math.random() * 250 },
      data: { label: `Action Node ${nodes.filter(node => node.id.startsWith('action')).length + 1}`, onChangeLabel: handleLabelChange },
      type: 'actionNode',
    };
    setNodes((nds) => [...nds, newNode]);
  };

  const handleLabelChange = (id, newLabel) => {
    setNodes((nds) =>
      nds.map((node) =>
        node.id === id ? { ...node, data: { ...node.data, label: newLabel } } : node
      )
    );
  };

  const handleEdgeLabelChange = (id, newLabel) => {
    setEdges((eds) =>
      eds.map((edge) =>
        edge.id === id ? { ...edge, label: newLabel } : edge
      )
    );
  };

  // Export Diagram function with desired format
  const exportDiagram = () => {
    // Map each node to the desired format
    const diagramData = nodes.map(node => {
      // Find edges where this node is the source
      const outgoingEdges = edges.filter(edge => edge.source === node.id);

      // Prepare buttons dictionary from outgoing edges
      const buttons = {};
      outgoingEdges.forEach(edge => {
        buttons[edge.label] = nodes.findIndex(n => n.id === edge.target) + 1;
      });

      // Structure the object for this node
      const nodeObject = {
        text: node.data.label,
      };

      // Add buttons if they exist for this node
      if (Object.keys(buttons).length > 0) {
        nodeObject.buttons = buttons;
      }

      return nodeObject;
    });

    // // Convert to JSON and download
    // const blob = new Blob([JSON.stringify(diagramData, null, 2)], { type: 'application/json' });
    // const url = URL.createObjectURL(blob);

    // const a = document.createElement('a');
    // a.href = url;
    // a.download = 'diagram.json';
    // a.click();
    // URL.revokeObjectURL(url);

    let jsonDiagramData = JSON.stringify(diagramData)
    console.log("Making post request with data to flask server");
    console.log({jsonDiagramData})

    let flask_server_url_data_endpoint = "http://127.0.0.1:5000/submit";
    fetch(
      flask_server_url_data_endpoint,
      {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonDiagramData,
      }
    )


  };

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <button onClick={addButtonNode} style={{ position: 'absolute', zIndex: 10, top: '10px', left: '10px' }}>
        Add Button
      </button>
      <button onClick={exportDiagram} style={{ position: 'absolute', zIndex: 10, top: '10px', right: '10px' }}>
        Export Diagram
      </button>
      <ReactFlow
        nodes={nodes}
        edges={edges.map(edge => ({
          ...edge,
          data: { label: edge.label, onChangeLabel: handleEdgeLabelChange },
          type: 'editableEdge',
        }))}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={{ buttonNode: ButtonNode, actionNode: ActionNode }}
        edgeTypes={{ editableEdge: EditableEdge }}
      >
        <Controls />
        <MiniMap />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  );
}