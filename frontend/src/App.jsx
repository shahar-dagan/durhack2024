import React, { useCallback, useState } from 'react';
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
const initialEdges = [{ id: 'e1-2', source: 'button-1', target: 'action-1' }];

// Custom component for "Button" nodes
function ButtonNode({ id, data, isConnectable }) {
  const [isEditing, setIsEditing] = useState(false);
  const [label, setLabel] = useState(data.label);

  const onDoubleClick = () => setIsEditing(true);
  const onBlur = () => {
    data.onChangeLabel(id, label); // Updates the main state
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

// Custom component for "Action" nodes
function ActionNode({ id, data, isConnectable }) {
  const [isEditing, setIsEditing] = useState(false);
  const [label, setLabel] = useState(data.label);

  const onDoubleClick = () => setIsEditing(true);
  const onBlur = () => {
    data.onChangeLabel(id, label); // Updates the main state
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

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // Function to add a new "Button" node
  const addButtonNode = () => {
    const newNode = {
      id: `button-${nodes.filter(node => node.id.startsWith('button')).length + 1}`,
      position: { x: Math.random() * 250, y: Math.random() * 250 },
      data: { label: `Button Node ${nodes.filter(node => node.id.startsWith('button')).length + 1}`, onChangeLabel: handleLabelChange },
      type: 'buttonNode',
    };
    setNodes((nds) => [...nds, newNode]);
  };

  // Function to add a new "Action" node
  const addActionNode = () => {
    const newNode = {
      id: `action-${nodes.filter(node => node.id.startsWith('action')).length + 1}`,
      position: { x: Math.random() * 250, y: Math.random() * 250 },
      data: { label: `Action Node ${nodes.filter(node => node.id.startsWith('action')).length + 1}`, onChangeLabel: handleLabelChange },
      type: 'actionNode',
    };
    setNodes((nds) => [...nds, newNode]);
  };

  // Function to update the label of a node in the main nodes state
  const handleLabelChange = (id, newLabel) => {
    setNodes((nds) =>
      nds.map((node) =>
        node.id === id ? { ...node, data: { ...node.data, label: newLabel } } : node
      )
    );
  };

  // Function to export the diagram as JSON
  const exportDiagram = () => {
    const diagramData = {
      nodes: nodes.map(node => ({
        id: node.id,
        type: node.type,
        label: node.data.label,
        position: node.position,
      })),
      edges: edges.map(edge => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
      })),
    };

    const blob = new Blob([JSON.stringify(diagramData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'diagram.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <button onClick={addButtonNode} style={{ position: 'absolute', zIndex: 10, top: '10px', left: '10px' }}>
        Add Button Node
      </button>
      <button onClick={addActionNode} style={{ position: 'absolute', zIndex: 10, top: '10px', left: '120px' }}>
        Add Action Node
      </button>
      <button onClick={exportDiagram} style={{ position: 'absolute', zIndex: 10, top: '10px', right: '10px' }}>
        Export Diagram
      </button>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={{ buttonNode: ButtonNode, actionNode: ActionNode }}
      >
        <Controls />
        <MiniMap />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  );
}
