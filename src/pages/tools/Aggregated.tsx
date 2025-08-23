import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, Upload, AlertCircle } from 'lucide-react';
import { useAnalytics } from '../../contexts/AnalyticsContext';
import { DataProcessor } from '../../lib/dataProcessing';
import { fileUtils } from '../../lib/fileUtils';
import FileUpload from '../../components/FileUpload';
import DataTable from '../../components/DataTable';
import LoadingSpinner from '../../components/LoadingSpinner';
import { ExtractedPriority } from '../../types';
import toast from 'react-hot-toast';

const Aggregated: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [masterFile, setMasterFile] = useState<File | null>(null);
  const [extractedData, setExtractedData] = useState<ExtractedPriority[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const { track } = useAnalytics();

  useEffect(() => {
    track('tool_accessed', { tool: 'Aggregated' });
  }, []);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setExtractedData([]);
    track('file_uploaded', { tool: 'Aggregated', filename: file.name, size: file.size });
  };

  const handleMasterFileSelect = (file: File) => {
    setMasterFile(file);
    track('master_file_uploaded', { tool: 'Aggregated', filename: file.name });
  };

  const handleFileRemove = () => {
    setSelectedFile(null);
    setExtractedData([]);
  };

  const handleMasterFileRemove = () => {
    setMasterFile(null);
  };

  const processFile = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    try {
      const rawData = await fileUtils.parseFile(selectedFile);
      
      // Validate required columns
      const requiredColumns = ['Priority Description', 'Usecase', 'Functional Workload', 'Company'];
      const firstRow = rawData[0] || {};
      const missingColumns = requiredColumns.filter(col => !(col in firstRow));
      
      if (missingColumns.length > 0) {
        throw new Error(`Missing required columns: ${missingColumns.join(', ')}`);
      }

      const processed = await DataProcessor.processAggregated(rawData);
      
      // Process master file if provided
      if (masterFile) {
        const masterData = await fileUtils.parseFile(masterFile);
        // Add vertical mapping logic here if needed
      }
      
      setExtractedData(processed);
      
      track('file_processed', { 
        tool: 'Aggregated', 
        filename: selectedFile.name,
        recordsProcessed: processed.length,
        hasMasterFile: !!masterFile
      });
      
      toast.success(`Successfully processed ${processed.length} priority records!`);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Processing failed';
      toast.error(message);
      track('processing_error', { tool: 'Aggregated', error: message });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = (format: 'csv' | 'excel') => {
    if (extractedData.length === 0) return;
    
    const filename = fileUtils.generateFilename('aggregated_priorities', format);
    
    if (format === 'csv') {
      fileUtils.downloadCSV(extractedData, filename);
    } else {
      fileUtils.downloadExcel(extractedData, filename);
    }
    
    track('file_downloaded', { tool: 'Aggregated', format, filename });
    toast.success(`Downloaded ${format.toUpperCase()} file successfully!`);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-full mb-4">
          <BarChart3 className="h-8 w-8 text-purple-600" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Aggregated Priority Extraction</h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Process aggregated priority data with advanced analytics and usecase mapping
        </p>
      </motion.div>

      {/* Instructions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card bg-purple-50 border-purple-200"
      >
        <div className="flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 text-purple-600 mt-0.5" />
          <div>
            <h3 className="font-medium text-purple-900 mb-2">Required File Format</h3>
            <p className="text-sm text-purple-800 mb-3">
              Your main file must contain the following columns:
            </p>
            <div className="grid grid-cols-2 md:grid-cols-2 gap-2 text-sm text-purple-700 mb-4">
              <span className="font-mono bg-purple-100 px-2 py-1 rounded">Priority Description</span>
              <span className="font-mono bg-purple-100 px-2 py-1 rounded">Usecase</span>
              <span className="font-mono bg-purple-100 px-2 py-1 rounded">Functional Workload</span>
              <span className="font-mono bg-purple-100 px-2 py-1 rounded">Company</span>
            </div>
            <p className="text-sm text-purple-800">
              Optionally upload a master company schema file for enhanced vertical mapping.
            </p>
          </div>
        </div>
      </motion.div>

      {/* File Upload */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h3 className="text-lg font-medium text-gray-900 mb-4">Main Priority File</h3>
          <FileUpload
            onFileSelect={handleFileSelect}
            selectedFile={selectedFile || undefined}
            onFileRemove={handleFileRemove}
            disabled={isProcessing}
          />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <h3 className="text-lg font-medium text-gray-900 mb-4">Master Schema (Optional)</h3>
          <FileUpload
            onFileSelect={handleMasterFileSelect}
            selectedFile={masterFile || undefined}
            onFileRemove={handleMasterFileRemove}
            disabled={isProcessing}
          />
        </motion.div>
      </div>

      {/* Process Button */}
      {selectedFile && !isProcessing && extractedData.length === 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="text-center"
        >
          <button
            onClick={processFile}
            className="btn-primary text-lg px-8 py-3"
          >
            <Upload className="h-5 w-5 mr-2" />
            Process Aggregated Data
          </button>
        </motion.div>
      )}

      {/* Processing State */}
      {isProcessing && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="card text-center py-12"
        >
          <LoadingSpinner size="lg" text="Processing aggregated data..." />
        </motion.div>
      )}

      {/* Results */}
      {extractedData.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              Extracted Priorities ({extractedData.length} records)
            </h2>
          </div>
          
          <DataTable
            data={extractedData}
            onDownload={handleDownload}
          />
        </motion.div>
      )}
    </div>
  );
};

export default Aggregated;